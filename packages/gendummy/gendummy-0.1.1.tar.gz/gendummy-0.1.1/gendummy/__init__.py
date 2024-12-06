# gendummy/__init__.py

from .gd import Gendummy

# Create a single instance of Gendummy
gd_instance = Gendummy()


# Expose methods from the instance
def gendf_auto(cols, rows):
    """Generate an automatic DataFrame with random integers and floats."""
    return gd_instance.gendf_auto(cols, rows)


def gendf_manual(cols, rows, dtypes):
    """Generate a manual DataFrame based on specified data types."""
    return gd_instance.gendf_manual(cols, rows, dtypes)


def genxls_auto(cols, rows):
    """Generate an Excel file from an automatically generated DataFrame."""
    gd_instance.genxls_auto(cols, rows)


def genxls_manual(cols, rows, dtypes):
    """Generate an Excel file from a manually generated DataFrame."""
    gd_instance.genxls_manual(cols, rows, dtypes)
