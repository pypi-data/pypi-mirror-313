# tests/test_import.py

import gendummy as gd


def test_gendf_auto():
    # Generate an automatic DataFrame
    df = gd.gendf_auto(cols=3, rows=3)
    print("Automatic DataFrame:")
    print(df)

    # Assertions to check the DataFrame structure
    assert df.shape == (3, 3)  # Check if the DataFrame has 3 rows and 3 columns
    assert "Col_0" in df.columns  # Ensure 'Col_0' is in the DataFrame


def test_gendf_manual():
    # Generate a manual DataFrame
    dtypes = [str, int]  # Example data types
    df_manual = gd.gendf_manual(cols=3, rows=3, dtypes=dtypes)
    print("Manual DataFrame:")
    print(df_manual)

    # Assertions to check the DataFrame structure
    assert df_manual.shape == (3, 3)  # Check if the DataFrame has 3 rows and 3 columns
    assert "Col_0" in df_manual.columns  # Ensure 'Col_0' is in the DataFrame


# Run tests
if __name__ == "__main__":
    test_gendf_auto()
    test_gendf_manual()
