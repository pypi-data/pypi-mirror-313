import pandas as pd
import random
import numpy as np

# Set a seed for reproducibility
random.seed(42)
np.random.seed(42)


class Gendummy:
    def gendf_auto(self, cols, rows):
        data = {}
        data[f"Col_0"] = [
            f"Item {i}" for i in range(rows)
        ]  # First column with string items

        for col in range(1, cols):
            if random.choice([True, False]):
                # Generate random integers
                data[f"Col_{col}"] = np.random.randint(
                    0, 100, size=rows
                )  # Random integers between 0 and 99
            else:
                # Generate random floats
                data[f"Col_{col}"] = (
                    np.random.rand(rows) * 100
                )  # Random floats between 0 and 100

        # Create the DataFrame
        return pd.DataFrame(data)

    def gendf_manual(self, cols, rows, dtypes):
        data = {}
        for col in range(cols):
            dt = dtypes[
                col % len(dtypes)
            ]  # Cycle through dtypes if there are fewer dtypes than cols

            if dt == str:
                # Generate a column of strings
                data[f"Col_{col}"] = [f"Item {i}" for i in range(rows)]
            elif dt == int:
                # Generate a column of random integers
                data[f"Col_{col}"] = np.random.randint(
                    0, 100, size=rows
                )  # Random integers between 0 and 99
            elif dt == float:
                # Generate a column of random floats
                data[f"Col_{col}"] = (
                    np.random.rand(rows) * 100
                )  # Random floats between 0 and 100

        # Create the DataFrame
        return pd.DataFrame(data)

    def genxls_auto(self, cols, rows):
        df = self.gendf_auto(cols, rows)
        df.to_excel("dummy_a.xlsx")

    def genxls_manual(self, cols, rows, dtypes):
        df = self.gendf_manual(cols, rows, dtypes)
        df.to_excel("dummy_m.xlsx")


# Module-level functions that users can call directly
def gendf_auto(cols, rows):
    """Display statistics for the given DataFrame."""
    gendummy = Gendummy()  # Create an instance of Statistics
    return gendummy.gendf_auto(cols, rows)
