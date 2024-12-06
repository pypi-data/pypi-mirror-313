
## Synopsis

This library provides a simple python interface to the heliophysics data 
and services of 
NASA's [Coordinated Data Analysis System](https://cdaweb.gsfc.nasa.gov/)
(CDAS).  This library implements the client side of the 
[CDAS RESTful web services](https://cdaweb.gsfc.nasa.gov/WebServices/REST/)
and can return data from any of 
[these datasets](https://cdaweb.gsfc.nasa.gov/misc/Notes.html) in a 
[SpacePy datamodel](https://spacepy.github.io/datamodel.html),
[xarray.Dataset](https://docs.xarray.dev/en/stable/generated/xarray.Dataset.html), or
[pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)
with all source and 
[ISTP/SPDF](https://spdf.gsfc.nasa.gov/sp_use_of_cdf.html) metadata.
Frequently asked questions concerning this library are at 
[FAQ](https://cdaweb.gsfc.nasa.gov/WebServices/REST/py/FAQ.html).
For more general details about the CDAS web services, see
https://cdaweb.gsfc.nasa.gov/WebServices/REST/.

## Code Example

This package contains example code calling most of the available web services.
To run the included example, do the following

    python -m cdasws

---
Also, the following [Jupyter notebooks](https://jupyter.org/) demonstrate
different features of the library:

1. [Data Retrieval](https://cdaweb.gsfc.nasa.gov/WebServices/REST/jupyter/CdasWsDataRetrieval.html) ([ipynb file](https://cdaweb.gsfc.nasa.gov/WebServices/REST/jupyter/CdasWsDataRetrieval.ipynb)) demonstrating use of library with results returned in [SpacePy data model](https://spacepy.github.io/datamodel.html), [xarray.Dataset](https://docs.xarray.dev/en/stable/generated/xarray.Dataset.html), and [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html). [Launch on Binder](https://binder.opensci.2i2c.cloud/v2/gh/berniegsfc/cdasws-notebooks/main?labpath=CdasWsDataRetrieval.ipynb).
2. [CDAWeb Binning Example](https://cdaweb.gsfc.nasa.gov/WebServices/REST/jupyter/CdasWsBinningExample.html) ([ipynb file](https://cdaweb.gsfc.nasa.gov/WebServices/REST/jupyter/CdasWsBinningExample.ipynb)) demonstrating use [CDAWeb binning](https://cdaweb.gsfc.nasa.gov/CDAWeb_Binning_readme.html). [Launch on Binder](https://binder.opensci.2i2c.cloud/v2/gh/berniegsfc/cdasws-notebooks/main?labpath=CdasWsBinningExample.ipynb).
3. [Magnetic Field Line Conjunction Example](https://sscweb.gsfc.nasa.gov/WebServices/REST/jupyter/SscWsConjunctionExample.html) ([ipynb file](https://sscweb.gsfc.nasa.gov/WebServices/REST/jupyter/SscWsConjunctionExample.ipynb)) with related data retrieval/plotting using [cdasws](https://pypi.org/project/cdasws/). [Launch on Binder](https://binder.opensci.2i2c.cloud/v2/gh/berniegsfc/sscws-notebooks/main?labpath=SscWsConjunctionExample.ipynb).
---

And at the bottom of each 
[CDAWeb dataset description](https://cdaweb.gsfc.nasa.gov/misc/Notes.html) 
is a "Data Access Code Examples" link that contains dataset-specific code 
utilizing this package to access the data.

## Motivation

This library hides the HTTP, JSON/XML, and CDF details of the CDAS web 
services. A python developer only has to deal with python objects and 
methods (primarily the SpacePy data model or xarray.Dataset object with 
full ISTP/SPDF metadata).

## Dependencies

The only required dependencies are python-dateutil and requests.  If you
call the get_data method then **one** of the following two sets of additional
dependencies are required:

1. To have get_data return the data in the SpacePy data model.
    * [SpacePy](https://spacepy.github.io/). Refer to the SpacePy
      documentation for the details of SpacePy's dependencies.
2. To have get_data return the data in an [xarray.Dataset](https://docs.xarray.dev/en/stable/generated/xarray.Dataset.html) or [pandas.DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html).
    * [cdflib](https://pypi.org/project/cdflib/).
    * [xarray](https://pypi.org/project/xarray/).

## Installation

As noted in the dependencies above, if you intend to call the get_data
method, you must install **one** of the following options.

1. [SpacePy](https://spacepy.github.io/).

        $ pip install -U spacepy

2. [cdflib](https://pypi.org/project/cdflib/) and [xarray](https://pypi.org/project/xarray/).

        $ pip install -U cdflib
        $ pip install -U xarray

Then, to install this package

    $ pip install -U cdasws


## API Reference

Refer to
[cdasws package API reference](https://cdaweb.gsfc.nasa.gov/WebServices/REST/py/cdasws/index.html)

or use the standard python help mechanism.

    from cdasws import CdasWs
    help(CdasWs)

## Tests

The tests directory contains 
[unittest](https://docs.python.org/3/library/unittest.html)
tests.

## Contributors

Bernie Harris.  
[e-mail](mailto:NASA-SPDF-Support@nasa.onmicrosoft.com) for support.

## License

This code is licensed under the 
[NASA Open Source Agreement](https://cdaweb.gsfc.nasa.gov/WebServices/NASA_Open_Source_Agreement_1.3.txt) (NOSA).
