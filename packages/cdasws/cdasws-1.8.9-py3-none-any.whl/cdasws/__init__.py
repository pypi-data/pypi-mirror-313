#!/usr/bin/env python3

#
# NOSA HEADER START
#
# The contents of this file are subject to the terms of the NASA Open
# Source Agreement (NOSA), Version 1.3 only (the "Agreement").  You may
# not use this file except in compliance with the Agreement.
#
# You can obtain a copy of the agreement at
#   docs/NASA_Open_Source_Agreement_1.3.txt
# or
#   https://cdaweb.gsfc.nasa.gov/WebServices/NASA_Open_Source_Agreement_1.3.txt.
#
# See the Agreement for the specific language governing permissions
# and limitations under the Agreement.
#
# When distributing Covered Code, include this NOSA HEADER in each
# file and include the Agreement file at
# docs/NASA_Open_Source_Agreement_1.3.txt.  If applicable, add the
# following below this NOSA HEADER, with the fields enclosed by
# brackets "[]" replaced with your own identifying information:
# Portions Copyright [yyyy] [name of copyright owner]
#
# NOSA HEADER END
#
# Copyright (c) 2018-2024 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#


"""
Package for accessing the Coordinate Data Analysis System (CDAS)
web services <https://cdaweb.gsfc.nasa.gov/WebServices/REST/>.<br>

Copyright &copy; 2018-2024 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.

Notes
-----
<ul>
  <li>Due to rate limiting implemented by the CDAS web services, an
      attempt to make simultaneous requests from many threads is likely
      to actually reduce performance.  At this time, it is best to make
      calls from five or fewer threads.</li>
  <li>Since CDAS data has datetime values with a UTC timezone, all
      client provided datetime values should have a timezone of UTC.
      If a given value's timezone is not UTC, the value is adjusted to
      UTC.  If a given value has no timezone (is naive), a UTC timezone
      is set.</li>
</ul>
"""


import sys
import os
import platform
import logging
import re
from importlib.util import find_spec
import urllib.parse
from urllib.parse import urlparse
import json
from operator import itemgetter
import time
from datetime import datetime, timedelta, timezone
import xml.etree.ElementTree as ET
from tempfile import mkstemp
from typing import Any, Callable, Dict, List, Tuple, Union

import requests
import dateutil.parser

from cdasws.datarepresentation import DataRepresentation
from cdasws.datarequest import AudioRequest, DataRequest
from cdasws.datarequest import CdfFormat, CdfRequest, Compression
from cdasws.datarequest import ImageFormat, GraphOptions, GraphRequest
from cdasws.datarequest import TextFormat, TextRequest, ThumbnailRequest
from cdasws.timeinterval import TimeInterval


# requires python >= 3.4
#if find_spec('spacepy.datamodel') is not None:
#    import spacepy.datamodel as spdm    # type: ignore
#    SPDM_AVAILABLE = True
#else:
#    SPDM_AVAILABLE = False
# python < 3.4
try:
    import spacepy.datamodel as spdm    # type: ignore
    SPDM_AVAILABLE = True
except ImportError:
    SPDM_AVAILABLE = False

try:
    from cdflib.xarray import cdf_to_xarray
    import xarray as xr
    CDF_XARRAY_AVAILABLE = True
except ImportError:
    try:
        import cdflib as cdf
        import xarray as xr
        CDF_XARRAY_AVAILABLE = True
        def cdf_to_xarray(filename, to_datetime=False, to_unixtime=False,
                          fillval_to_nan=False):
            """
            Reads a CDF into an xarray.dataset.  This function exists
            to provide compatility with cdflib >= 1.0.1 for older
            releases of cdflib.

            Parameters:
            -----------
            filename
                The path to the CDF file to read.
            to_datetime
                Whether or not to convert CDF_EPOCH/EPOCH_16/TT2000 to
                datetime, or leave them as is.
            to_unixtime
                Whether or not to convert CDF_EPOCH/EPOCH_16/TT2000 to
                unixtime, or leave them as is.
            fillval_to_nan
                If True, any data values that match the FILLVAL
                attribute for a variable will be set to NaN.

            Returns
            -------
            xarray.dataset
                An XArray Dataset object.
            """
            return cdf.cdf_to_xarray(filename, to_datetime=to_datetime,
                                     to_unixtime=to_unixtime,
                                     fillval_to_nan=fillval_to_nan)
    except ImportError:
        CDF_XARRAY_AVAILABLE = False


__version__ = "1.8.9"


#
# Limit on the number of times an HTTP request which returns a
# 429 or 503 status with a Retry-After header will be retried.
#
RETRY_LIMIT = 100

#
# XML schema namespace
#
NS = 'http://cdaweb.gsfc.nasa.gov/schema'
#
# XHTML schema namespace
#
XHTML_NS = 'http://www.w3.org/1999/xhtml'
#
# All namespaces found in responses.
#
NAMESPACES = {
    'cdas': NS,
    'xhtml': XHTML_NS
}


def _get_data_progress(
        progress: float,
        msg: str,
        value: Dict) -> int:
    """
    A get_data progress callback which adjusts the progress value for
    the download portion of a larger operation and then calls the
    "real" progress callback function with this adjusted progress value.

    Parameters
    ----------
    progress
        Measure of progress.
    msg
        Message describing progress of get_data call.
    value
        Dictionary containing the function to call and values for
        computing the adjusted progress value.
    Returns
    -------
    int
        Flag indicating whether to continue with getting the data.
        0 to continue. 1 to abort getting the data.
    """
    progress_callback = value.get('progressCallback', None)
    progress_user_value = value.get('progressUserValue', None)
    adjusted_progress = value['progressStart'] + \
                        value['progressFraction'] * progress

    if progress_callback is not None:

        return progress_callback(adjusted_progress, msg,
                                 progress_user_value)
    return 0


class NullAuth(requests.auth.AuthBase): # pylint: disable=too-few-public-methods
    """
    Authentication class used to cause requests to ignore any ~/.netrc
    file.  The CDAS web services do not support authentication and
    a cdaweb (ftps) entry will cause CdasWs requests to fail with
    a 401 error.  See <https://github.com/psf/requests/issues/2773>.
    """
    def __call__(self, r):
        return r


class CdasWs:
    """
    Class representing the web service interface to NASA's
    Coordinated Data Analysis System (CDAS)
    <https://cdaweb.gsfc.nasa.gov>.

    Notes
    -----
    The logger used by this class has the class' name (CdasWs).  By default,
    it is configured with a NullHandler.  Users of this class may configure
    the logger to aid in diagnosing problems.
    """
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    def __init__(
            self,
            endpoint=None,
            timeout=None,
            proxy=None,
            ca_certs=None,
            disable_ssl_certificate_validation=False,
            user_agent=None):
        """
        Creates an object representing the CDAS web services.

        Parameters
        ----------
        endpoint
            URL of the CDAS web service.  If None, the default is
            'https://cdaweb.gsfc.nasa.gov/WS/cdasr/1/dataviews/sp_phys/'.
        timeout
            Number of seconds to wait for a response from the server.
        proxy
            HTTP proxy information.  For example,<pre>
            proxies = {
              'http': 'http://10.10.1.10:3128',
              'https': 'http://10.10.1.10:1080',
            }</pre>
            Proxy information can also be set with environment variables.
            For example,<pre>
            $ export HTTP_PROXY="http://10.10.1.10:3128"
            $ export HTTPS_PROXY="http://10.10.1.10:1080"</pre>
        ca_certs
            Path to certificate authority (CA) certificates that will
            override the default bundle.
        disable_ssl_certificate_validation
            Flag indicating whether to validate the SSL certificate.
        user_agent
            A value that is appended to the HTTP User-Agent value.
        """

        self.logger = logging.getLogger(type(self).__name__)
        self.logger.addHandler(logging.NullHandler())

        self.logger.debug('endpoint = %s', endpoint)
        self.logger.debug('ca_certs = %s', ca_certs)
        self.logger.debug('disable_ssl_certificate_validation = %s',
                          disable_ssl_certificate_validation)

        if endpoint is None:
            self._endpoint = 'https://cdaweb.gsfc.nasa.gov/WS/cdasr/1/dataviews/sp_phys/'
        else:
            self._endpoint = endpoint

        self._user_agent = 'cdasws/' + __version__ + ' (' + \
            platform.python_implementation() + ' ' \
            + platform.python_version() + '; ' + platform.platform() + ')'

        if user_agent is not None:
            self._user_agent += ' (' + user_agent + ')'

        self._request_headers = {
            #'Content-Type' : 'application/json',
            'Content-Type' : 'application/xml',
            'Accept' : 'application/xml',
            'User-Agent' : self._user_agent,
            #'Accept-Encoding' : 'gzip'  # only beneficial for icdfml responses
        }
        self._session = requests.Session()
        self._session.headers.update(self._request_headers)
        self._session.auth = NullAuth()

        if ca_certs is not None:
            self._session.verify = ca_certs

        if disable_ssl_certificate_validation is True:
            self._session.verify = False

        if proxy is not None:
            self._proxy = proxy

        self._timeout = timeout

        endpoint_components = urlparse(self._endpoint)
        self._hdp_registry = endpoint_components.scheme + '://' + \
            endpoint_components.netloc + '/registry/hdp/SscId.xql'

    # pylint: enable=too-many-arguments


    def __del__(self):
        """
        Destructor.  Closes all network connections.
        """

        self.close()


    def close(self) -> None:
        """
        Closes any persistent network connections.  Generally, deleting
        this object is sufficient and calling this method is unnecessary.
        """
        self._session.close()


    def get_observatory_groups(
            self,
            **keywords: str
        ) -> List[Dict]:
        """
        Gets descriptions of the observatory groups from the server.

        Parameters
        ----------
        keywords
            optional keyword parameters as follows:<br>
            <b>instrumentType</b> - an instrument type value from those
            returned by `CdasWs.get_instrument_types`.  Omitting
            this parameter indicates that no observatories are eliminated
            based upon their instrumentType value.
        Returns
        -------
        List
            An array of ObservatoryGroupDescription
            dictionaries where the structure of the dictionary mirrors
            ObservatoryGroupDescription in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """
        if 'instrumentType' in keywords:
            url = self._endpoint + 'observatoryGroups?instrumentType=' + \
                      urllib.parse.quote(keywords['instrumentType'])
        else:
            url = self._endpoint + 'observatoryGroups'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('response.text = %s', response.text)

        observatory_response = ET.fromstring(response.text)

        observatory_group_descriptions = []
        for description in observatory_response.findall(\
            'cdas:ObservatoryGroupDescription', namespaces=NAMESPACES):

            observatory_ids = []
            for observatory_id in description.findall(\
                'cdas:ObservatoryId', namespaces=NAMESPACES):

                observatory_ids.append(observatory_id.text)

            observatory_group_descriptions.append({
                'Name': description.find(\
                    'cdas:Name', namespaces=NAMESPACES).text,
                'ObservatoryId': observatory_ids
            })

        return observatory_group_descriptions


    def get_instrument_types(
            self,
            **keywords: str
        ) -> List[Dict]:
        """
        Gets descriptions of the instrument types from the server.

        Parameters
        ----------
        keywords
            optional keyword parameters as follows:<br>
            <b>observatory</b> - an observatory value from those returned
            by `CdasWs.get_observatories`.  Omitting this parameter
            indicates that no instrumentTypes are eliminated based upon
            their observatory value.<br>
            <b>observatoryGroup</b> - an observatory group value from
            those returned by `CdasWs.get_observatory_groups`.  Omitting
            this parameter indicates that no instrumentTypes are
            eliminated based upon their observatoryGroup value.</br>
        Returns
        -------
        List
            An array of InstrumentTypeDescription
            dictionaries where the structure of the dictionary mirrors
            InstrumentTypeDescription in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """
        if 'observatory' in keywords:
            url = self._endpoint + 'instrumentTypes?observatory=' \
                  + urllib.parse.quote(keywords['observatory'])
        elif 'observatoryGroup' in keywords:
            url = self._endpoint + 'instrumentTypes?observatoryGroup=' \
                  + urllib.parse.quote(keywords['observatoryGroup'])
        else:
            url = self._endpoint + 'instrumentTypes'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('response.text = %s', response.text)

        instrument_response = ET.fromstring(response.text)

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('instrument_response = %s',
                              ET.tostring(instrument_response))

        instrument_types = []
        for description in instrument_response.findall(\
            'cdas:InstrumentTypeDescription', namespaces=NAMESPACES):

            instrument_types.append({
                'Name': description.find('cdas:Name',
                                         namespaces=NAMESPACES).text
                })
        return instrument_types


    def get_instruments(
            self,
            **keywords: str
        ) -> List[Dict]:
        """
        Gets descriptions of the instruments from the server.

        Parameters
        ----------
        keywords
            optional keyword parameters as follows:<br>
            <b>observatory</b> - an observatory value from those returned
            by `CdasWs.get_observatories`.  Omitting this parameter
            indicates that no instruments are eliminated based upon their
            observatory value.<br>
            <b>instrumentType</b> - an instrument type value from those
            returned by `CdasWs.get_instrument_types`.  Omitting this
            parameter indicates that no instruments are eliminated based
            upon their instrument type.<br>
        Returns
        -------
        List
            An array of InstrumentDescription
            dictionaries where the structure of the dictionary mirrors
            InstrumentDescription in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """
        if 'observatory' in keywords:
            url = self._endpoint + 'instruments?observatory=' \
                  + urllib.parse.quote(keywords['observatory'])
        elif 'instrumentType' in keywords:
            url = self._endpoint + 'instruments?instrumentType=' \
                  + urllib.parse.quote(keywords['instrumentType'])
        else:
            url = self._endpoint + 'instruments'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('response.text = %s', response.text)

        instruments_response = ET.fromstring(response.text)

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('instruments = %s', response.text)
                              #ET.indent(instruments_response, space='    '))

        instruments = []
        for instrument_description in instruments_response.findall(\
            'cdas:InstrumentDescription', namespaces=NAMESPACES):

            instruments.append({
                'Name': instrument_description.find(\
                    'cdas:Name', namespaces=NAMESPACES).text,
                'ShortDescription': instrument_description.find(\
                    'cdas:ShortDescription', namespaces=NAMESPACES).text,
                'LongDescription': instrument_description.find(\
                    'cdas:LongDescription', namespaces=NAMESPACES).text
            })

        return instruments


    def get_observatories(
            self,
            **keywords: str
        ) -> List[Dict]:
        """
        Gets descriptions of the observatories from the server.

        Parameters
        ----------
        keywords
            optional keyword parameters as follows:<br>
            <b>instrument</b> - an instrument value from those returned
            by `CdasWs.get_instruments`.  Omitting this parameter
            indicates that no observatories are eliminated based upon
            their instrument value.<br>
            <b>instrumentType</b> - in instrument type value from those
            returned by `CdasWs.get_instrument_types`.  Omitting this
            parameter indicates that no observatories are eliminated
            based upon their instrumentType value.<br>
        Returns
        -------
        List
            An array of ObservatoryDescriptions
            dictionaries where the structure of the dictionary mirrors
            ObservatoryDescription in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """
        if 'instrument' in keywords:
            url = self._endpoint + 'observatories?instrument=' \
                  + urllib.parse.quote(keywords['instrument'])
        elif 'instrumentType' in keywords:
            url = self._endpoint + 'observatories?instrumentType=' \
                  + urllib.parse.quote(keywords['instrumentType'])
        else:
            url = self._endpoint + 'observatories'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('response.text = %s', response.text)

        observatory_response = ET.fromstring(response.text)

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('observatories = %s', response.text)

        observatories = []

        for observatory in observatory_response.findall(\
            'cdas:ObservatoryDescription', namespaces=NAMESPACES):
            observatories.append({
                'Name': observatory.find(\
                    'cdas:Name', namespaces=NAMESPACES).text,
                'ShortDescription': observatory.find(\
                    'cdas:ShortDescription', namespaces=NAMESPACES).text,
                'LongDescription': observatory.find(\
                    'cdas:LongDescription', namespaces=NAMESPACES).text
            })

        return observatories


    def get_observatory_groups_and_instruments(
            self,
            **keywords: str
        ) -> List[Dict]:
        """
        Gets descriptions of the observatory groups (and associated
        instruments) from the server.

        Parameters
        ----------
        keywords
            optional keyword parameters as follows:<br>
            <b>instrumentType</b> - an instrument type value from those
            returned by `CdasWs.get_instrument_types`.  Omitting this
            parameter indicates that no observatories are eliminated
            based upon their instrumentType value.<br>
        Returns
        -------
        List
            An array of ObservatoryGroupInstrumentDescription
            dictionaries where the structure of the dictionary mirrors
            ObservatoryGroupInstrumentDescription in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """
        if 'instrumentType' in keywords:
            url = self._endpoint \
                  + 'observatoryGroupsAndInstruments?instrumentType=' \
                  + urllib.parse.quote(keywords['instrumentType'])
        else:
            url = self._endpoint + 'observatoryGroupsAndInstruments'

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('response.text = %s', response.text)

        observatories_response = ET.fromstring(response.text)

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('observatories = %s', response.text)

        o_g_i_ds = []

        for o_g_i_d in observatories_response.findall(\
            'cdas:ObservatoryGroupInstrumentDescription',\
            namespaces=NAMESPACES):

            o_g_i_d_name = o_g_i_d.find('cdas:Name',
                                        namespaces=NAMESPACES).text
            o_is = []
            for o_i in o_g_i_d.findall('cdas:ObservatoryInstruments',
                                       namespaces=NAMESPACES):

                o_i_name = o_i.find('cdas:Name',
                                    namespaces=NAMESPACES).text
                i_ds = []
                for i_d in o_i.findall('cdas:InstrumentDescription',
                                       namespaces=NAMESPACES):
                    i_d_name = i_d.find('cdas:Name',
                                        namespaces=NAMESPACES).text
                    i_d_short_description = \
                        i_d.find('cdas:ShortDescription',
                                 namespaces=NAMESPACES).text
                    i_d_long_description = \
                         i_d.find('cdas:LongDescription',
                                  namespaces=NAMESPACES).text
                    i_ds.append({
                        'Name': i_d_name,
                        'ShortDescription': i_d_short_description,
                        'LongDescription': i_d_long_description
                    })
                o_is.append({
                    'Name': o_i_name,
                    'InstrumentDescription': i_ds
                })

            o_g_i_ds.append({
                'Name': o_g_i_d_name,
                'ObservatoryInstruments': o_is
            })

        return o_g_i_ds


    # pylint: disable=too-many-branches
    def get_datasets(
            self,
            **keywords: str
        ) -> List[Dict]:
        """
        Gets descriptions of the specified datasets from the server.

        Parameters
        ----------
        keywords
            optional keyword parameters as follows:<br>
            <b>observatoryGroup</b> - an observatory group value from those
            returned by `CdasWs.get_observatory_groups`.  Omitting this
            parameter
            indicates that no datasets are eliminated based upon their
            observatoryGroup value.<br>
            <b>instrumentType</b> - an instrument type value from those
            returned by `CdasWs.get_instrument_types`.  Omitting this
            parameter indicates that no datasets are eliminated based
            upon their instrumentType value.<br>
            <b>observatory</b> - an observatory name value from those
            returned by `CdasWs.get_observatories`.  Omitting this
            parameter indicates that no datasets are eliminated based
            upon their observatory value.<br>
            <b>instrument</b> - an instrument value from those returned by
            `CdasWs.get_instruments`.  Omitting this parameter indicates
            that no datasets are eliminated based upon their instrument
            value.<br>
            <b>startDate</b> - a datetime specifying the start of a time
            interval.  See module note about timezone value.  If this
            parameter is ommited, the time interval will begin infinitely
            in the past.<br>
            <b>stopDate</b> - a datetime specifying the end of a time
            interval.  See module note about timezone value.  If this
            parameter is omitted, the time interval will end infinitely
            in the future.<br>
            <b>id</b> - a dataset identifier. The value may be a CDAS
            (e.g., AC_H2_MFI), DOI (e.g., 10.48322/fh85-fj47), or SPASE
            [ResourceID] (e.g., spase://NASA/NumericalData/ACE/MAG/L2/PT1H)
            identifier. If specified, all other keywords are ignored.<br>
            <b>idPattern</b> - a java.util.regex compatible regular
            expression that must match the dataset's CDAS identifier value.
            Omitting this parameter is equivalent to `.*`.<br>
            <b>labelPattern</b> - a java.util.regex compatible regular
            expression that must match the dataset's CDAS label text.
            Omitting this parameter is equivalent to `.*`.  Embedded
            matching flag expressions (e.g., `(?i)` for case insensitive
            match mode) are supported and likely to be useful in this
            case.<br>
            <b>notesPattern</b> - a java.util.regex compatible regular
            expression that must match the dataset's CDAS notes text.
            Omitting this parameter is equivalent to `.*`.  Embedded
            matching flag expressions (e.g., `(?s)` for dotall match mode)
            are supported and likely to be useful in this case.<br>
        Returns
        -------
        List
            A list of dictionaries containing descriptions of the datasets
            requested.  The dictionary structure is defined by the
            DatasetDescription element in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """
        url = self._endpoint + 'datasets?'

        observatory_groups = keywords.get('observatoryGroup', None)
        if observatory_groups is not None:
            if isinstance(observatory_groups, str):
                observatory_groups = [observatory_groups]
            for observatory_group in observatory_groups:
                url = url + 'observatoryGroup=' \
                      + urllib.parse.quote(observatory_group) + '&'

        instrument_types = keywords.get('instrumentType', None)
        if instrument_types is not None:
            if isinstance(instrument_types, str):
                instrument_types = [instrument_types]
            for instrument_type in instrument_types:
                url = url + 'instrumentType=' \
                      + urllib.parse.quote(instrument_type) + '&'

        observatories = keywords.get('observatory', None)
        if observatories is not None:
            if isinstance(observatories, str):
                observatories = [observatories]
            for observatory in observatories:
                url = url + 'observatory=' \
                      + urllib.parse.quote(observatory) + '&'

        instruments = keywords.get('instrument', None)
        if instruments is not None:
            if isinstance(instruments, str):
                instruments = [instruments]
            for instrument in instruments:
                url = url + 'instrument=' \
                      + urllib.parse.quote(instrument) + '&'

        if 'startDate' in keywords:
            url = url + 'startDate=' \
                  + urllib.parse.quote(keywords['startDate']) + '&'

        if 'stopDate' in keywords:
            url = url + 'stopDate=' \
                  + urllib.parse.quote(keywords['stopDate']) + '&'

        if 'id' in keywords:
            url = url + 'id=' \
                  + urllib.parse.quote(keywords['id']) + '&'

        if 'idPattern' in keywords:
            url = url + 'idPattern=' \
                  + urllib.parse.quote(keywords['idPattern']) + '&'

        if 'labelPattern' in keywords:
            url = url + 'labelPattern=' \
                  + urllib.parse.quote(keywords['labelPattern']) + '&'

        if 'notesPattern' in keywords:
            url = url + 'notesPattern=' \
                  + urllib.parse.quote(keywords['notesPattern']) + '&'

        self.logger.debug('request url = %s', url[:-1])

        response = self._session.get(url[:-1], timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('response.text = %s', response.text)

        dss = ET.fromstring(response.text)

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('datasets = %s', response.text)

        datasets = []
        for ds in dss.findall('cdas:DatasetDescription',
                              namespaces=NAMESPACES):

            observatory_groups = []
            for o_g in ds.findall('cdas:ObservatoryGroup',
                                  namespaces=NAMESPACES):
                observatory_groups.append(o_g.text)

            instrument_types = []
            for i_t in ds.findall('cdas:InstrumentType',
                                  namespaces=NAMESPACES):
                instrument_types.append(i_t.text)

            dataset_links = []
            for d_l in ds.findall('cdas:DatasetLink',
                                  namespaces=NAMESPACES):
                dataset_links.append({
                    'Title': d_l.find('cdas:Title',
                                      namespaces=NAMESPACES).text,
                    'Text': d_l.find('cdas:Text',
                                     namespaces=NAMESPACES).text,
                    'Url': d_l.find('cdas:Url',
                                    namespaces=NAMESPACES).text,
                })

            observatories = []
            for obs_elem in ds.findall('cdas:Observatory',
                                       namespaces=NAMESPACES):
                observatories.append(obs_elem.text)

            instruments = []
            for instr_elem in ds.findall('cdas:Instrument',
                                         namespaces=NAMESPACES):
                instruments.append(instr_elem.text)

            dataset = {
                'Id': ds.find('cdas:Id', namespaces=NAMESPACES).text,
                'Observatory': observatories,
                'Instrument': instruments,
                'ObservatoryGroup': observatory_groups,
                'InstrumentType': instrument_types,
                'Label': ds.find('cdas:Label',
                                 namespaces=NAMESPACES).text,
                'TimeInterval': {
                    'Start': ds.find('cdas:TimeInterval/cdas:Start',
                                     namespaces=NAMESPACES).text,
                    'End': ds.find('cdas:TimeInterval/cdas:End',
                                   namespaces=NAMESPACES).text
                },
                'PiName': ds.find('cdas:PiName',
                                  namespaces=NAMESPACES).text,
                'PiAffiliation': ds.find('cdas:PiAffiliation',
                                         namespaces=NAMESPACES).text,
                'Notes': ds.find('cdas:Notes',
                                 namespaces=NAMESPACES).text,
                'DatasetLink': dataset_links
            }
            doi = ds.find('cdas:Doi', namespaces=NAMESPACES)
            if doi is not None:
                dataset['Doi'] = doi.text

            spase_resource_id = ds.find('cdas:SpaseResourceId',
                                        namespaces=NAMESPACES)
            if spase_resource_id is not None:
                dataset['SpaseResourceId'] = spase_resource_id.text

            additional_metadata = []
            for add_meta in ds.findall('cdas:AdditionalMetadata',
                                       namespaces=NAMESPACES):
                meta_type = add_meta.attrib['Type']
                value = add_meta.text
                additional_metadata.append({
                    'Type': meta_type,
                    'value': value
                })

            if len(additional_metadata) > 0:
                dataset['AdditionalMetadata'] = additional_metadata

            datasets.append(dataset)

        return sorted(datasets, key=itemgetter('Id'))
    # pylint: enable=too-many-branches


    @staticmethod
    def get_doi_landing_page_url(
            doi: str
        ) -> str:
        """
        Returns a URL to the given Digital Object Identifier's landing
        page (metadata for the DOI).

        Parameters
        ----------
        doi
            digital object identifier.
        Returns
        -------
        str
            A URL to the DOI's landing page.
        """

        if not doi.startswith('http'):
            return 'https://doi.org/' + doi
        return doi


    @staticmethod
    def get_citation(
            doi: str
        ) -> str:
        """
        Returns the citation from doi.org for the given DOI.

        Parameters
        ----------
        doi
            digital object identifier.
        Returns
        -------
        str
            The citation from doi.org for the given DOI.
        """

        url = 'https://doi.org/' + doi
        headers = {'Accept': 'text/x-bibliography; style=apa'}
        response = requests.get(url, headers=headers)

        return response.text


    def get_inventory(
            self,
            identifier: str,
            **keywords: str
        ) -> List[TimeInterval]:
        """
        Gets a description of the specified dataset's data inventory.

        Parameters
        ----------
        identifier
            dataset identifier of data inventory to get.
        keywords
            optional keyword parameters as follows:<br>
            <b>timeInterval</b> - `timeinterval.TimeInterval` to restrict
            returned inventory.
        Returns
        -------
        List
            An array of `timeinterval.TimeInterval`s when data is
            available.
        """

        url = self._endpoint + 'datasets/' + \
                  urllib.parse.quote(identifier, safe='') + '/inventory'

        if 'timeInterval' in keywords:
            time_interval_keyword = keywords['timeInterval']
            url = url + '/' + \
                  TimeInterval.basic_iso_format(time_interval_keyword.start) + \
                  ',' + \
                  TimeInterval.basic_iso_format(time_interval_keyword.end)

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('response.text = %s', response.text)

        inventory = ET.fromstring(response.text)
        intervals = []
        for inventory_desc in inventory.findall(\
                                  'cdas:InventoryDescription',
                                  namespaces=NAMESPACES):
            for time_interval in inventory_desc.findall(\
                                     'cdas:TimeInterval',
                                     namespaces=NAMESPACES):
                intervals.append(
                    TimeInterval(
                        time_interval.find('cdas:Start',
                                           namespaces=NAMESPACES).text,
                        time_interval.find('cdas:End',
                                           namespaces=NAMESPACES).text
                    )
                )

        return intervals


    def get_example_time_interval(
            self,
            identifier: str,
        ) -> TimeInterval:
        """
        Gets a small example time interval for the specified dataset.  The
        interval is near the end of the dataset's data inventory.  The
        returned interval is not guaranteed to have non-fill data for any
        specific variable.

        Parameters
        ----------
        identifier
            dataset identifier of data inventory to get.
        Returns
        -------
        timeinterval.TimeInterval
            An small example time interval that is likely, but not
            guaranteed, to have data or None if an interval cannot be
            found.
        """

        time_intervals = self.get_inventory(identifier)
        if len(time_intervals) < 1:
            return None
        example_interval = time_intervals[-1]
        if re.search('MMS[1-4]_.+_BRST_.+', identifier):
            time_delta = timedelta(seconds=1)
        else:
            time_delta = timedelta(hours=2)
        example_interval.start = example_interval.end - time_delta
        return example_interval


    def get_variables(
            self,
            identifier: str
        ) -> List[Dict]:
        """
        Gets a description of the variables in the specified dataset.

        Parameters
        ----------
        identifier
            dataset identifier of data to get.
        Returns
        -------
        List
            A List of dictionary descriptions of the variables in
            the specified dataset.  The dictionary structure is defined by
            the VariableDescription element in
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        """

        url = self._endpoint + 'datasets/' + \
                  urllib.parse.quote(identifier, safe='') + '/variables'

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return []

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('response.text = %s', response.text)

        var_descriptions = ET.fromstring(response.text)

        variables = []
        for var_description in var_descriptions.findall(\
                                   'cdas:VariableDescription',
                                   namespaces=NAMESPACES):
            name = var_description.find('cdas:Name',
                                        namespaces=NAMESPACES).text
            short_description = var_description.find(\
                                        'cdas:ShortDescription',
                                        namespaces=NAMESPACES).text
            if short_description is None:
                short_description = ''

            long_description = var_description.find(\
                                        'cdas:LongDescription',
                                        namespaces=NAMESPACES).text
            if long_description is None:
                long_description = ''

            variables.append({
                'Name': name,
                'ShortDescription': short_description,
                'LongDescription': long_description
            })

        return variables


    def get_variable_names(
            self,
            identifier: str
        ) -> List[str]:
        """
        Gets the names of the variables in the specified dataset.  This
        method is like the get_variables method except that it only returns
        the variable names and not the other metadata.

        Parameters
        ----------
        identifier
            dataset identifier of data to get.
        Returns
        -------
        List
            A List of the names of the variables in the specified dataset.
        """

        variable_names = []
        for variable in self.get_variables(identifier):
            variable_names.append(variable['Name'])

        return variable_names


    @staticmethod
    def _get_thumbnail_description_dict(
            file_description_elem: ET.Element
        ) -> Dict:
        """
        Gets ThumbnailDescription dictionary representation from the
        given FileDescription element.

        Parameters
        ----------
        file_description_elem
            a FileDescription Element.
        Returns
        -------
        Dict
            a Dictionary representation of the ThumbnailDescription
            contained in the given FileDescription element.
        """
        thumbnail_desc = file_description_elem.find(\
                             'cdas:ThumbnailDescription',
                             namespaces=NAMESPACES)
        if thumbnail_desc is not None:
            time_interval = thumbnail_desc.find('cdas:TimeInterval',
                                                namespaces=NAMESPACES)
            start = time_interval.find('cdas:Start',
                                       namespaces=NAMESPACES).text
            end = time_interval.find('cdas:End',
                                     namespaces=NAMESPACES).text
            return {
                'Name': thumbnail_desc.find('cdas:Name',
                                            namespaces=NAMESPACES).text,
                'Dataset': thumbnail_desc.find('cdas:Dataset',
                                               namespaces=NAMESPACES).text,
                'TimeInterval': {
                    'Start': start,
                    'End': end
                },
                'VarName': thumbnail_desc.find('cdas:VarName',
                                               namespaces=NAMESPACES).text,
                'Options': int(thumbnail_desc.find(\
                                   'cdas:Options',
                                   namespaces=NAMESPACES).text),
                'NumFrames': int(thumbnail_desc.find(\
                                     'cdas:NumFrames',
                                     namespaces=NAMESPACES).text),
                'NumRows': int(thumbnail_desc.find(\
                                   'cdas:NumRows',
                                   namespaces=NAMESPACES).text),
                'NumCols': int(thumbnail_desc.find(\
                                   'cdas:NumCols',
                                   namespaces=NAMESPACES).text),
                'TitleHeight': int(thumbnail_desc.find(\
                                       'cdas:TitleHeight',
                                       namespaces=NAMESPACES).text),
                'ThumbnailHeight': int(thumbnail_desc.find(\
                                           'cdas:ThumbnailHeight',
                                           namespaces=NAMESPACES).text),
                'ThumbnailWidth': int(thumbnail_desc.find(\
                                           'cdas:ThumbnailWidth',
                                           namespaces=NAMESPACES).text),
                'StartRecord': int(thumbnail_desc.find(\
                                       'cdas:StartRecord',
                                       namespaces=NAMESPACES).text),
                'MyScale': float(thumbnail_desc.find(\
                                     'cdas:MyScale',
                                     namespaces=NAMESPACES).text),
                'XyStep': float(thumbnail_desc.find(\
                                    'cdas:XyStep',
                                    namespaces=NAMESPACES).text)
            }
        return None


    @staticmethod
    def _get_data_result_dict(
            xml_data_result: str
        ) -> Dict:
        """
        Gets DataResult dictionary representation from the
        given XML DataResult element.

        Parameters
        ----------
        xml_data_result
            XML representation of a DataResult.
        Returns
        -------
        Dict
            a Dictionary representation of the given XML representation
            of a DataResult.
        """
        data_result = ET.fromstring(xml_data_result)
        file_descriptions = []
        for file_description in data_result.findall(\
            'cdas:FileDescription', namespaces=NAMESPACES):

            dict_file_description = {
                'Name': file_description.find('cdas:Name',
                                              namespaces=NAMESPACES).text,
                'MimeType': file_description.find(\
                                'cdas:MimeType',
                                namespaces=NAMESPACES).text,
                'StartTime': file_description.find(\
                                 'cdas:StartTime',
                                 namespaces=NAMESPACES).text,
                'EndTime': file_description.find(\
                               'cdas:EndTime',
                               namespaces=NAMESPACES).text,
                'Length': int(file_description.find(\
                                  'cdas:Length',
                                  namespaces=NAMESPACES).text),
                'LastModified': file_description.find(\
                                    'cdas:LastModified',
                                    namespaces=NAMESPACES).text
            }
            thumbnail_dict = CdasWs._get_thumbnail_description_dict(\
                                     file_description)
            if thumbnail_dict is not None:
                dict_file_description['ThumbnailDescription'] = \
                    thumbnail_dict

            thumbnail_id_elem = file_description.find(\
                                    'cdas:ThumbnailId',
                                    namespaces=NAMESPACES)
            if thumbnail_id_elem is not None:
                dict_file_description['ThumbnailId'] = \
                    thumbnail_id_elem.text

            file_descriptions.append(dict_file_description)

        if len(file_descriptions) > 0:
            return {
                'FileDescription': file_descriptions
            }
        return None


    def get_data_result(
            self,
            data_request: DataRequest,
            progress_callback: Callable[[float, str, Any], int],
            progress_user_value: Any
        ) -> Tuple[int, Dict]:
        """
        Submits the given request to the server and returns the result.
        This is a relatively low-level method and most callers should
        probably use a higher-level method such as get_data.

        Parameters
        ----------
        data_request
            data request.
        progress_callback
            function that is called repeatedly to report the progress
            of getting the data.  The function should return 0 if it
            wants to continue getting data.  If it returns a non-0 value,
            getting the data will be aborted and the get_data() function
            will immediately return (204, None).  The float parameter
            is a value between 0.0 and 1.0 to indicate progress and
            the str parameter will contain a text message indicating
            the progress of this call.
        progressUserValue
            value that is passsed to the progressCallback function.
        Returns
        -------
        Tuple
            [0] contains the int HTTP status code.  200 when
            successful.<br>
            [1] contains a dictionary representing the DataResult from
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>
            or None.
        See Also
        --------
        CdasWs.get_data
        """

        #self.logger.debug('data_request = %s', data_request.json())
        self.logger.debug('data_request = %s', data_request.xml_str())

        url = self._endpoint + 'datasets'

        for retries in range(RETRY_LIMIT):
            #response = self._session.post(url, data=data_request.json(),
            response = self._session.post(url, data=data_request.xml_str(),
                                          timeout=self._timeout)

            if response.status_code == 200:

                data_result = CdasWs._get_data_result_dict(response.text)

                if not data_result:
                    return (response.status_code, None)

                return (response.status_code, data_result)

            if response.status_code == 429 or \
               response.status_code == 503 and \
               'Retry-After' in response.headers:

                retry_after = response.headers['Retry-After']

                self.logger.debug('429/503 status with Retry-After header: %s',
                                  retry_after)

                if progress_callback is not None:
                    if progress_callback(0.2, 'Waiting ' + retry_after + \
                                         's before making server request.',
                                         progress_user_value) != 0:
                        return (204, None)

                retry_after = int(retry_after)

                self.logger.info('Sleeping %d seconds before making request',
                                 retry_after)
                time.sleep(retry_after)

            else:
                self.logger.info('%s failed with http code %d', url,
                                 response.status_code)
                self.logger.info('data_request = %s', data_request)
                self.logger.info('response.text: %s', response.text)
                return (response.status_code, None)

        self.logger.info('%s failed with http code %d after %d retries',
                         url, response.status_code, retries + 1)
        self.logger.info('data_request = %s', data_request)
        self.logger.info('response.text: %s', response.text)
        return (response.status_code, None)


    def get_data_file(
            self,
            dataset: str,
            variables: List[str],
            start: Union[datetime, str], end: Union[datetime, str],
            **keywords: Union[
                Dict,
                Callable[[float, str, Any], int],
                Any]
        ) -> Tuple[int, Dict]:
        """
        Gets the specified data file from the server.

        Parameters
        ----------
        dataset
            dataset identifier of data to get.
        variables
            array containing names of variables to get.
        start
            start time of data to get.  See module note about timezone.
        end
            end time of data to get.  See module note about timezone.
        keywords
            optional keyword parameters as follows:<br>
            <b>binData</b> - indicates that uniformly spaced values should
            be computed for scaler/vector/spectrogram data according to
            the given binning parameter values.  binData is a Dict that
            may contain the following keys: interval,
            interpolateMissingValues, sigmaMultiplier, and/or
            overrideDefaultBinning with values that override the
            defaults.<br>
            <b>progressCallback</b> - is a
            Callable[[float, str, typing.Any], int]
            function that is called repeatedly to report the progress
            of getting the data.  The function should return 0 if it
            wants to continue getting data.  If it returns non-0 value,
            getting the data will be aborted and the get_data_file()
            function will immediately return (204, None).  The float
            parameter is a value between 0.0 and 1.0 to indicate progress
            and the str parameter will contain a text message indicating
            the progress of this call.<br>
            <b>progressUserValue</b> - is an Any value that is passsed
            to the progressCallback function.<br>
        Returns
        -------
        Tuple
            [0] contains the int HTTP status code.  200 when
            successful.<br>
            [1] contains a dictionary representing the DataResult from
            <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>
            or None.
        Raises
        ------
        ValueError
            If the given start/end datetime values are invalid.
        See Also
        --------
        CdasWs.get_data : In addition to what get_data_file does,
            get_data also downloads and reads the data file into memory
            (SpaceData or xarray.Dataset object).
        """
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-return-statements
        # pylint: enable=too-many-statements
        # pylint: disable=too-many-branches

        start_datetime, end_datetime = TimeInterval.get_datetimes(start,
                                                                  end)

        data_request = CdfRequest(dataset, variables,
                                  TimeInterval(start_datetime,
                                               end_datetime),
                                  3, CdfFormat.BINARY,
                                  **keywords.get('binData', {}))

        progress_callback = keywords.get('progressCallback', None)
        progress_user_value = keywords.get('progressUserValue', None)

        self.logger.debug('data_request = %s', data_request)

        if progress_callback is not None:
            if progress_callback(0.1, 'Making server request.',
                                 progress_user_value) != 0:
                return (204, None)

        status_code, data_result = self.get_data_result(data_request,
                                                        progress_callback,
                                                        progress_user_value)

        if progress_callback is not None:
            if progress_callback(1.0, 'Initial server request complete.',
                                 progress_user_value) != 0:
                return (status_code, None)

        return (status_code, data_result)


    def download(
            self,
            url: str,
            size: int = 0,
            **keywords
        ) -> str:
        """
        Downloads the file specified by the given URL to a temporary
        file without reading all of it into memory.  This method
        utilizes the connection pool and persistent HTTP connection
        to the CdasWs server.

        Parameters
        ----------
        url
            URL of file to download.
        size
            number of bytes in file to download.
        keywords
            optional keyword parameters as follows:<br>
            <b>progressCallback</b> - is a
            typing.Callable[[float, str, typing.Any], int]
            function that is called repeatedly to report the progress
            of getting the data.  The function should return 0 if it
            wants to continue getting data.  If it returns a non-0 value,
            getting the data will be aborted and this download() function
            will immediately return None.  The float parameter
            is a value between 0.0 and 1.0 to indicate progress and
            the str parameter will contain a text message indicating
            the progress of this call.<br>
            <b>progressUserValue</b> - is a typing.Any value that is
            passsed to the progressCallback function.<br>
        Returns
        -------
        str
            name of tempory file or None if there was an error.
        """
        # pylint: disable=too-many-locals

        progress_callback = keywords.get('progressCallback', None)
        progress_user_value = keywords.get('progressUserValue', None)

        suffix = os.path.splitext(urlparse(url).path)[1]

        file_descriptor, tmp_filename = mkstemp(suffix=suffix)

        download_bytes = 0
        next_progress_report = 0.1
        with self._session.get(url, stream=True,
                               timeout=self._timeout) as response:

            file = open(tmp_filename, 'wb')
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    file.write(chunk)
                    # file.flush()
                    if progress_callback is not None:
                        download_bytes += len(chunk)
                        if size == 0:
                            download_progress = 0.0
                        else:
                            download_progress = float(download_bytes) / size
                        if download_progress > next_progress_report:
                            next_progress_report += download_progress
                            if progress_callback(download_progress,\
                                   'Continuing download of data.',
                                                 progress_user_value) != 0:

                                file.close()
                                os.close(file_descriptor)
                                return None
            file.close()
            os.close(file_descriptor)

        if progress_callback is not None:
            if progress_callback(0.4,
                                 'Data download complete. Reading data.',
                                 progress_user_value) != 0:
                return None

        return tmp_filename


    @staticmethod
    def read_data(
            filename: str,
            data_representation: DataRepresentation
        ) -> Union['spacepy.datamodel', 'xr.Dataset']:
        """
        Reads the data from the given file.

        Parameters
        ----------
        filename
            Name of file to read.
        data_representation
            Requested data representation.
        Returns
        -------
        spacepy.datamodel or xr.Dataset
            Data from file.
        Raises
        ------
        Exception
            If an Exception is raise by either the spdm.fromCDF() or
            cdflib.cdf_to_xarray() functions.
        ModuleNotFoundError
            If the required spacepy.datamodel or the cdflib and xarray
            modules are not installed.
        """
        if data_representation is None:
            if SPDM_AVAILABLE:
                return spdm.fromCDF(filename)
            if CDF_XARRAY_AVAILABLE:
                return cdf_to_xarray(filename, to_datetime=True,
                                     fillval_to_nan=True)
            raise ModuleNotFoundError(
                'neither the spacepy.datamodel nor the cdflib and '
                'xarray modules are installed')

        if data_representation is DataRepresentation.SPACEPY and \
           not SPDM_AVAILABLE:
            raise ModuleNotFoundError('spacepy module must be installed')
        if data_representation is DataRepresentation.XARRAY and \
           not CDF_XARRAY_AVAILABLE:
            raise ModuleNotFoundError('cdflib and xarray modules must be installed')

        if data_representation is DataRepresentation.SPACEPY:
            return spdm.fromCDF(filename)
        if data_representation is DataRepresentation.XARRAY:
            return cdf_to_xarray(filename, to_datetime=True,
                                 fillval_to_nan=True)
        return None


    def get_data(
            self,
            dataset: str,
            variables: List[str],
            time0: Union[TimeInterval, List[TimeInterval], datetime, str],
            time1: Union[datetime, str] = None,
            **keywords: Union[
                Dict,
                DataRepresentation,
                Callable[[float, str, Any], int],
                Any]
        ) -> Tuple[Dict, 'spdm.SpaceData', 'xarray']:
        """
        Gets the specified data from the server.  The representation
        of the returned data is determined as follows:<br>
        1. If a dataRepresentation keyword parameter is given, its
           value will determine the representation of the returned
           data.  If no dataRepresenation keyword parameter is
           given, then<br>
        2. If the presence of spacepy.datamodel is found, then the data
           is returned in the spacepy.datamodel representation.<br>
        3. If the presence of the cdflib and xarray modules are found,
           then the data is returned in an xarray.Dataset.

        Parameters
        ----------
        dataset
            dataset identifier of data to get.
        variables
            array containing names of variables to get.  The value
            ALL-VARIABLES may be used instead of specifying all the
            individual variable names.
        time0
            TimeInterval(s) or start time of data to get.  See module
            note about timezone.
        time1
            when time0 is not one or more TimeInterval(s), the end time
            of data to get.  See module note about timezone.
        keywords
            optional keyword parameters as follows:<br>
            <b>binData</b> - indicates that uniformly spaced values should
            be computed for scaler/vector/spectrogram data according to
            the given binning parameter values.  See
            <https://cdaweb.gsfc.nasa.gov/CDAWeb_Binning_readme.html>
            for more details.  binData is a Dict that
            may contain the following keys: interval,
            interpolateMissingValues, sigmaMultiplier, and/or
            overrideDefaultBinning with values that override the
            defaults.<br>
            <b>dataRepresentation</b> - specifies the representation of
            the returned data as one of
            `datarepresentation.DataRepresentation`.<br>
            <b>progressCallback</b> - is a
            Callable[[float, str, typing.Any], int]
            function that is called repeatedly to report the progress
            of getting the data.  The function should return 0 if it
            wants to continue getting data.  If it returns non-0 value,
            getting the data will be aborted and the get_data() function
            will immediately return (204, None).  The float parameter
            is a value between 0.0 and 1.0 to indicate progress and
            the str parameter will contain a text message indicating
            the progress of this call.<br>
            <b>progressUserValue</b> - is an Any value that is passsed
            to the progressCallback function.<br>
        Returns
        -------
        Tuple
            [0] contains a dictionary of HTTP and CDAS status information.
            When successful, ['http']['status_code'] will be 200.<br>
            [1] contains the requested data (SpaceData or xarray.Dataset
            object) or None.
        Raises
        ------
        ValueError
            If no variables are given or if the given start/end datetime
            values are invalid.
        """
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-return-statements
        # pylint: disable=too-many-statements
        # pylint: disable=too-many-branches
        # pylint: disable=import-outside-toplevel

        #import spacepy.datamodel as spdm       # type: ignore

        if len(variables) < 1:
            raise ValueError('at least one variable name is required')

        if isinstance(time0, (str, datetime)):
            if isinstance(time1, (str, datetime)):
                time_intervals = [TimeInterval(time0, time1)]
            else:
                raise ValueError('time1 must be str/datetime')
        elif isinstance(time0, TimeInterval):
            time_intervals = [time0]
        elif isinstance(time0, list) and len(time0) > 0 and\
             isinstance(time0[0], TimeInterval):
            time_intervals = time0
        else:
            raise ValueError('invalid time0 type')

        data_request = CdfRequest(dataset, variables,
                                  time_intervals,
                                  3, CdfFormat.BINARY,
                                  binData=keywords.get('binData', {}))

        data_rep = keywords.get('dataRepresentation', None)
        progress_callback = keywords.get('progressCallback', None)
        progress_user_value = keywords.get('progressUserValue', None)

        self.logger.debug('data_request = %s', data_request)

        status = {
            'http': {
                'status_code': 204
            },
            'cdas': {
                'status': [],
                'message': [],
                'warning': [],
                'error': []
            }
        }

        if progress_callback is not None:
            if progress_callback(0.1, 'Making initial server request.',
                                 progress_user_value) != 0:
                return (status, None)

        status_code, data_result = self.get_data_result(data_request,
                                                        progress_callback,
                                                        progress_user_value)

        status['http']['status_code'] = status_code

        if progress_callback is not None:
            if progress_callback(0.3, 'Initial server request complete.',
                                 progress_user_value) != 0:
                return (status, None)

        if status_code != 200:

            self.logger.info('get_data_result failed with http code %d',
                             status_code)
            self.logger.info('data_request = %s', data_request)
            return (status, None)

        if not data_result:
            return (status, None)

        if 'Status' in data_result:
            status['cdas']['status'] = data_result['Status']
        if 'Message' in data_result:
            status['cdas']['message'] = data_result['Message']
        if 'Warning' in data_result:
            status['cdas']['warning'] = data_result['Warning']
        if 'Error' in data_result:
            status['cdas']['error'] = data_result['Error']

        if progress_callback is not None:
            if progress_callback(0.4, 'Beginning download of data.',
                                 progress_user_value) != 0:
                return (status, None)

        file_descriptions = data_result['FileDescription']

        data_url = file_descriptions[0]['Name']
        data_length = file_descriptions[0]['Length']

        self.logger.debug('data_url = %s, data_length = %d',
                          data_url, data_length)

        sub_progress_control = {
            'progressCallback': progress_callback,
            'progressUserValue': progress_user_value,
            'progressStart': 0.4,
            'progressFraction': 0.1
        }

        tmp_filename = self.download(data_url, data_length,
                                     progressCallback=_get_data_progress,
                                     progressUserValue=sub_progress_control)

        try:
            data = self.read_data(tmp_filename, data_rep)
            os.remove(tmp_filename)
            if progress_callback is not None:
                if progress_callback(1.0, 'Finished reading data.',
                                     progress_user_value) != 0:
                    return (status, None)
        except:
            self.logger.error('Exception from read_data(%s): %s, %s',
                              tmp_filename, sys.exc_info()[0],
                              sys.exc_info()[1])
            self.logger.error('CDF file has been retained.')
            raise
        return (status, data)


    # pylint: disable=too-many-arguments
    def get_graph(
            self,
            dataset: str,
            variables: List[str],
            start: Union[datetime, str],
            end: Union[datetime, str],
            options: GraphOptions = None,
            image_format: List[ImageFormat] = None,
            **keywords
        ) -> Tuple[int, Dict]:
        """
        Gets a graphical representation of the specified data from the
        server.

        Parameters
        ----------
        dataset
            dataset identifier of data to get.
        variables
            array containing names of variables to get.
        start
            start time of data to get.  See module note about timezone.
        end
            end time of data to get.  See module note about timezone.
        options
            graph options.
        image_format
            image format.  If None, then [ImageFormat.PNG].
        keywords
            optional keyword parameters as follows:<br>
            <b>binData</b> - indicates that uniformly spaced values should
            be computed for scaler/vector/spectrogram data according to
            the given binning parameter values.  binData is a Dict that
            may contain the following keys: interval,
            interpolateMissingValues, sigmaMultiplier, and/or
            overrideDefaultBinning with values that override the
            defaults.<br>
            <b>progressCallback</b> - is a
            typing.Callable[[float, str, typing.Any], int]
            function that is called repeatedly to report the progress
            of getting the data.  The function should return 0 if it
            wants to continue getting data.  If it returns non-0 value,
            getting the data will be aborted and the get_data() function
            will immediately return (204, None).  The float parameter
            is a value between 0.0 and 1.0 to indicate progress and
            the str parameter will contain a text message indicating
            the progress of this call.<br>
            <b>progressUserValue</b> - is a typing.Any value that is
            passsed to the progressCallback function.<br>
        Returns
        -------
        Tuple
            [0] contains the HTTP status code value (200 when successful).<br>
            [1] contains a dictionary representation of a
                <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>
                DataResult object or None.<br>
        Raises
        ------
        ValueError
            If the given start/end datetime values are invalid.
        """
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-return-statements
        # pylint: enable=too-many-statements
        # pylint: disable=too-many-branches

        start_datetime, end_datetime = TimeInterval.get_datetimes(start,
                                                                  end)

        request = GraphRequest(dataset, variables,
                               TimeInterval(start_datetime, end_datetime),
                               options, image_format,
                               **keywords)

        progress_callback = keywords.get('progressCallback', None)
        progress_user_value = keywords.get('progressUserValue', None)

        self.logger.debug('request = %s', request)

        if progress_callback is not None:
            if progress_callback(0.1, 'Making server request.',
                                 progress_user_value) != 0:
                return (204, None)

        status_code, result = self.get_data_result(request, progress_callback, progress_user_value)

        if progress_callback is not None:
            if progress_callback(1.0, 'Server request complete.',
                                 progress_user_value) != 0:
                return (status_code, None)

        if status_code != 200:

            self.logger.info('get_result failed with http code %d',
                             status_code)
            self.logger.info('request = %s', request)
            return (status_code, None)

        return (status_code, result)
    # pylint: enable=too-many-arguments


    # pylint: disable=too-many-arguments
    def get_thumbnail(
            self,
            dataset: str,
            variables: List[str],
            start: Union[datetime, str],
            end: Union[datetime, str],
            identifier: str,
            thumbnail: int = 1,
            **keywords
        ) -> Tuple[int, Dict]:
        """
        Gets a graphical representation of the specified data from the
        server.

        Parameters
        ----------
        dataset
            dataset identifier of data to get.
        variables
            array containing names of variables to get.
        start
            start time of data to get.  See module note about timezone.
        end
            end time of data to get.  See module note about timezone.
        identifier
            thumbnail identifier (returned in a previous get_graph
            result).
        thumbnail
            number of thumbnail whose full size image is being requested.
            Thumbnail images are counted beginning at one (not zero).
        keywords
            optional keyword parameters as follows:<br>
            <b>progressCallback</b> - is a
            typing.Callable[[float, str, typing.Any], int]
            function that is called repeatedly to report the progress
            of getting the data.  The function should return 0 if it
            wants to continue getting data.  If it returns non-0 value,
            getting the data will be aborted and the get_data() function
            will immediately return (204, None).  The float parameter
            is a value between 0.0 and 1.0 to indicate progress and
            the str parameter will contain a text message indicating
            the progress of this call.<br>
            <b>progressUserValue</b> - is a typing.Any value that is
            passsed to the progressCallback function.<br>
        Returns
        -------
        Tuple
            [0] contains the HTTP status code value (200 when successful).<br>
            [1] contains a dictionary representation of a
                <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>
                DataResult object or None.<br>
        Raises
        ------
        ValueError
            If the given start/end datetime values are invalid.
        """
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-return-statements
        # pylint: enable=too-many-statements
        # pylint: disable=too-many-branches

        start_datetime, end_datetime = TimeInterval.get_datetimes(start,
                                                                  end)

        request = ThumbnailRequest(dataset, variables,
                                   TimeInterval(start_datetime, end_datetime),
                                   identifier, thumbnail)

        progress_callback = keywords.get('progressCallback', None)
        progress_user_value = keywords.get('progressUserValue', None)

        self.logger.debug('request = %s', request)

        if progress_callback is not None:
            if progress_callback(0.1, 'Making server request.',
                                 progress_user_value) != 0:
                return (204, None)

        status_code, result = self.get_data_result(request,
                                                   progress_callback,
                                                   progress_user_value)

        if progress_callback is not None:
            if progress_callback(1.0, 'Server request complete.',
                                 progress_user_value) != 0:
                return (status_code, None)

        if status_code != 200:

            self.logger.info('get_result failed with http code %d',
                             status_code)
            self.logger.info('request = %s', request)
            return (status_code, None)

        return (status_code, result)
    # pylint: enable=too-many-arguments


    # pylint: disable=too-many-arguments
    def get_text(
            self,
            dataset: str,
            variables: List[str],
            start: Union[datetime, str],
            end: Union[datetime, str],
            compression: Compression = Compression.UNCOMPRESSED,
            text_format: TextFormat = TextFormat.PLAIN,
            **keywords
        ) -> Tuple[int, Dict]:
        """
        Gets a textual representation of the specified data from the
        server.

        Parameters
        ----------
        dataset
            dataset identifier of data to get.
        variables
            array containing names of variables to get.
        start
            start time of data to get.  See module note about timezone.
        end
            end time of data to get.  See module note about timezone.
        compression
            file compression.
        text_format
            text format.
        keywords
            optional keyword parameters as follows:<br>
            <b>binData</b> - indicates that uniformly spaced values should
            be computed for scaler/vector/spectrogram data according to
            the given binning parameter values.  binData is a Dict that
            may contain the following keys: interval,
            interpolateMissingValues, sigmaMultiplier, and/or
            overrideDefaultBinning with values that override the
            defaults.<br>
            <b>progressCallback</b> - is a
            typing.Callable[[float, str, typing.Any], int]
            function that is called repeatedly to report the progress
            of getting the data.  The function should return 0 if it
            wants to continue getting data.  If it returns non-0 value,
            getting the data will be aborted and the get_data() function
            will immediately return (204, None).  The float parameter
            is a value between 0.0 and 1.0 to indicate progress and
            the str parameter will contain a text message indicating
            the progress of this call.<br>
            <b>progressUserValue</b> - is a typing.Any value that is
            passsed to the progressCallback function.<br>
        Returns
        -------
        Tuple
            [0] contains the HTTP status code value (200 when successful).<br>
            [1] contains a dictionary representation of a
                <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>
                DataResult object or None.<br>
        Raises
        ------
        ValueError
            If the given start/end datetime values are invalid.
        """
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-return-statements
        # pylint: enable=too-many-statements
        # pylint: disable=too-many-branches

        start_datetime, end_datetime = TimeInterval.get_datetimes(start,
                                                                  end)

        request = TextRequest(dataset, variables,
                              TimeInterval(start_datetime, end_datetime),
                              compression, text_format,
                              **keywords)

        progress_callback = keywords.get('progressCallback', None)
        progress_user_value = keywords.get('progressUserValue', None)

        self.logger.debug('request = %s', request)

        if progress_callback is not None:
            if progress_callback(0.1, 'Making server request.',
                                 progress_user_value) != 0:
                return (204, None)

        status_code, result = self.get_data_result(request,
                                                   progress_callback,
                                                   progress_user_value)

        if progress_callback is not None:
            if progress_callback(1.0, 'Server request complete.',
                                 progress_user_value) != 0:
                return (status_code, None)

        if status_code != 200:

            self.logger.info('get_result failed with http code %d',
                             status_code)
            self.logger.info('request = %s', request)
            return (status_code, None)

        return (status_code, result)
    # pylint: enable=too-many-arguments


    def get_audio(
            self,
            dataset: str,
            variables: List[str],
            start: Union[datetime, str],
            end: Union[datetime, str],
            **keywords
        ) -> Tuple[int, Dict]:
        """
        Gets an audio representation of the specified data from the
        server.

        Parameters
        ----------
        dataset
            dataset identifier of data to get.
        variables
            array containing names of variables to get.
        start
            start time of data to get.  See module note about timezone.
        end
            end time of data to get.  See module note about timezone.
        keywords
            optional keyword parameters as follows:<br>
            <b>binData</b> - indicates that uniformly spaced values should
            be computed for scaler/vector/spectrogram data according to
            the given binning parameter values.  binData is a Dict that
            may contain the following keys: interval,
            interpolateMissingValues, sigmaMultiplier, and/or
            overrideDefaultBinning with values that override the
            defaults.<br>
            <b>progressCallback</b> - is a
            typing.Callable[[float, str, typing.Any], int]
            function that is called repeatedly to report the progress
            of getting the data.  The function should return 0 if it
            wants to continue getting data.  If it returns non-0 value,
            getting the data will be aborted and the get_data() function
            will immediately return (204, None).  The float parameter
            is a value between 0.0 and 1.0 to indicate progress and
            the str parameter will contain a text message indicating
            the progress of this call.<br>
            <b>progressUserValue</b> - is a typing.Any value that is
            passsed to the progressCallback function.<br>
        Returns
        -------
        Tuple
            [0] contains the HTTP status code value (200 when successful).<br>
            [1] contains a dictionary representation of a
                <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>
                DataResult object or None.<br>
        Raises
        ------
        ValueError
            If the given start/end datetime values are invalid.
        """
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-return-statements
        # pylint: enable=too-many-statements
        # pylint: disable=too-many-branches

        start_datetime, end_datetime = TimeInterval.get_datetimes(start,
                                                                  end)

        request = AudioRequest(dataset, variables,
                               TimeInterval(start_datetime, end_datetime),
                               **keywords)

        progress_callback = keywords.get('progressCallback', None)
        progress_user_value = keywords.get('progressUserValue', None)

        self.logger.debug('request = %s', request)

        if progress_callback is not None:
            if progress_callback(0.1, 'Making server request.',
                                 progress_user_value) != 0:
                return (204, None)

        status_code, result = self.get_data_result(request,
                                                   progress_callback,
                                                   progress_user_value)

        if progress_callback is not None:
            if progress_callback(1.0, 'Server request complete.',
                                 progress_user_value) != 0:
                return (status_code, None)

        if status_code != 200:

            self.logger.info('get_result failed with http code %d',
                             status_code)
            self.logger.info('request = %s', request)
            return (status_code, None)

        return (status_code, result)


    def get_original_files(
            self,
            dataset: str,
            start: Union[datetime, str],
            end: Union[datetime, str],
            **keywords
        ) -> Tuple[int, Dict]:
        """
        Gets original data files from a dataset.  Original data files
        lack updated meta-data and virtual variable values contained
        in files obtained from the `CdasWs.get_data`.  Most callers
        should probably use `CdasWs.get_data` instead of this function.

        Parameters
        ----------
        dataset
            dataset identifier of data to get.
        start
            start time of data to get.  See module note about timezone.
        end
            end time of data to get.  See module note about timezone.
        keywords
            optional keyword parameters as follows:<br>
            <b>progressCallback</b> - is a
            typing.Callable[[float, str, typing.Any], int]
            function that is called repeatedly to report the progress
            of getting the data.  The function should return 0 if it
            wants to continue getting data.  If it returns non-0 value,
            getting the data will be aborted and the get_data() function
            will immediately return (204, None).  The float parameter
            is a value between 0.0 and 1.0 to indicate progress and
            the str parameter will contain a text message indicating
            the progress of this call.<br>
            <b>progressUserValue</b> - is a typing.Any value that is
            passsed to the progressCallback function.<br>
        Returns
        -------
        Tuple
            [0] contains the HTTP status code value (200 when successful).<br>
            [1] array of dictionary representations of a
                <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>
                FileDescription objects or None.<br>
        Raises
        ------
        ValueError
            If the given start/end datetime values are invalid.
        See Also
        --------
        CdasWs.get_data
        """
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-return-statements
        # pylint: enable=too-many-statements
        # pylint: disable=too-many-branches

        start_datetime, end_datetime = TimeInterval.get_datetimes(start,
                                                                  end)

        request = CdfRequest(dataset, [],
                             TimeInterval(start_datetime, end_datetime))

        progress_callback = keywords.get('progressCallback', None)
        progress_user_value = keywords.get('progressUserValue', None)

        self.logger.debug('request = %s', request)

        if progress_callback is not None:
            if progress_callback(0.1, 'Making server request.',
                                 progress_user_value) != 0:
                return (204, None)

        status_code, result = self.get_data_result(request,
                                                   progress_callback,
                                                   progress_user_value)

        if progress_callback is not None:
            if progress_callback(1.0, 'Server request complete.',
                                 progress_user_value) != 0:
                return (status_code, None)

        if status_code != 200:

            self.logger.info('get_result failed with http code %d',
                             status_code)
            self.logger.info('request = %s', request)
            return (status_code, None)

        return (status_code, result['FileDescription'])


    def get_ssc_id(
            self,
            dataset: str
        ) -> Tuple[int, Union[str, List[str]]]:
        """
        Gets the Satellite Situation Center (SSC)
        <https://sscweb.gsfc.nasa.gov/> observatory identifier(s)
        associated with the given cdaweb dataset identifier.

        Notes
        -----
        This method relies upon the Heliophysics Data Portal's
        <https://heliophysicsdata.gsfc.nasa.gov/> metadata.  That metadata
        may be incomplete.  Also, cdaweb has datasets for which SSC has
        no corresponding observatory (for example, ground observatory
        data).  Callers should be prepared for negative results (200, None)
        from this method.

        Parameters
        ----------
        dataset
            cdaweb dataset identifier.
        Returns
        -------
        Tuple
            [0] contains the HTTP status code value (200 when successful).<br>
            [1] the SSC observatory identifier(s) associated with the given
                cdaweb dataset identifier or None if none is found.
        """
        url = self._hdp_registry + '?cdawebId=' + dataset

        self.logger.debug('request url = %s', url)

        response = self._session.get(url, timeout=self._timeout)

        if response.status_code != 200:

            self.logger.info('%s failed with http code %d', url,
                             response.status_code)
            self.logger.info('response.text: %s', response.text)
            return (response.status_code, None)

        if self.logger.level <= logging.DEBUG:
            self.logger.debug('response.text = %s', response.text)

        results = ET.fromstring(response.text)

        ssc_id = []
        for ssc_id_elem in results.findall('SscId'):
            ssc_id.append(ssc_id_elem.text)

        if len(ssc_id) == 0:
            result = None
        elif len(ssc_id) == 1:
            result = ssc_id[0]
        else:
            result = ssc_id

        return (response.status_code, result)
