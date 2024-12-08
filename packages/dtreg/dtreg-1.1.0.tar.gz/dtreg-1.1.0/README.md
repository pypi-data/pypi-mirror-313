# dtreg
<!-- badges: start -->
[![PyPI version](https://badge.fury.io/py/dtreg.svg?cache-control=no-cache)](https://badge.fury.io/py/dtreg)
[![Coverage Status](https://coveralls.io/repos/github/OlgaLezhnina/dtreg_py/badge.svg?branch=master)](https://coveralls.io/github/OlgaLezhnina/dtreg_py?branch=master)

![Python](https://img.shields.io/badge/python-3.8-blue.svg)
<!-- badges: end -->

The goal of dtreg is to help users interact with various data type registries (DTRs) and create machine-readable data. 
Currently, we support the [ePIC](https://fc4e-t4-3.github.io/) and [ORKG](https://orkg.org/) DTRs.
* First, load a DTR schema (an ePIC datatype or an ORKG template) as a Python object.
* Then, create a new instance of the schema by filling in the relevant fields.
* Finally, write the instance as a machine-readable JSON-LD file. 
## Installation

```sh
## install from PyPi:
pip install dtreg
```

## Example

This example shows you how to work with a DTR schema.
You need to know the schema identifier; see the [help page](https://orkg.org/help-center/article/47/reborn_articles).
For instance, the schema “data item” requires the ePIC datatype with the DOI <https://doi.org/21.T11969/aff130c76e68ead3862e>.
For the ORKG, please use the ORKG template URL, such as <https://orkg.org/template/R758316>.

```python
## import functions from the dtreg
from dtreg.load_datatype import load_datatype
from dtreg.to_jsonld import to_jsonld
## import pandas for a dataframe
import pandas as pd
## load the schema with the known identifier
dt = load_datatype("https://doi.org/21.T11969/aff130c76e68ead3862e")
## look at the schemata you might need to use
dt.__dict__.keys() 
## check available fields for your schema
dt.data_item.prop_list 
## create your instance by filling the fields of your choice
## see the help page to know more about the fields
my_label = "my results"
my_df = pd.DataFrame({'A': [1], 'B': [2]})
my_df.name = "dataframe_name"
url_1 = dt.url(label = "URL_1")
url_2 = dt.url(label = "URL_2")
my_inst = dt.data_item(label=my_label,
                       has_expression=[url_1, url_2],
                       source_table=my_df)
## write the instance in JSON-LD format as a string
my_json = to_jsonld(my_inst) 

## the result can be saved as a JSON file
with open('my_file.json', 'w') as f:
    f.write(my_json)

```
For more information, please see the [help page](https://orkg.org/help-center/article/47/reborn_articles).