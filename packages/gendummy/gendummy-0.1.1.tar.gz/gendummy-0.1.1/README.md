# Gendummy

**Gendummy** is a Python library for generating dummy data in the form of pandas DataFrames or xlsx spreadsheets. It provides functionality to create both automatic and manually specified data tables. 

## Features

- Generate DataFrames with random data, where dtyps are defined automatically (col[0] is always str).
- Generate DataFrames with random data, where dtyps are defined manually.


## Installation

To use the Gendummy library, ensure you have Python and pip installed, then install the required package:

```bash
    pip install gendummy
```

## Import

```python
    import gendummy as gd
```

## Usage

```python
    df = gd.gendf_auto(cols=3, rows=3)
    df = gd.gendf_manual(cols=3, rows=3, dtypes=[str, float, str])
    gd.genxls_auto(cols=3, rows=3)
    gd.genxls_manual(cols=3, rows=3, dtypes=[str, float, str])

```