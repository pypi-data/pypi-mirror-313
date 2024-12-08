import polars as pl
import pandas as pd

class amvParameters:
    def __init__(self, **kwargs):
        # Set default parameters
        self.P0000 = kwargs.get('P0000', 4095)
        self.P0001 = kwargs.get('P0001', 5)
        self.P0002 = kwargs.get('P0002', 40)
        self.P0003 = kwargs.get('P0003', 40)
        self.P0004 = kwargs.get('P0004', 1)
        self.P0005 = kwargs.get('P0005', 50)
        self.P0006 = kwargs.get('P0006', 30)
        self.P0007 = kwargs.get('P0007', 1800)
        self.P0008 = kwargs.get('P0008', 100)
        self.P0009 = kwargs.get('P0009', 1)
        self.P000A = kwargs.get('P000A', 0)
        self.P000B = kwargs.get('P000B', 50)
        self.P000C = kwargs.get('P000C', 50)
        self.P000D = kwargs.get('P000D', 50)
        self.P000E = kwargs.get('P000E', 50)
        self.P000F = kwargs.get('P000F', 75)
        self.P0010 = kwargs.get('P0010', 55)
        self.P0011 = kwargs.get('P0011', 1)
        self.P0012 = kwargs.get('P0012', 50)
        self.P0013 = kwargs.get('P0013', 0)
        self.P0014 = kwargs.get('P0014', 0)
        self.P0015 = kwargs.get('P0015', 40)

class amvSignalAnalysis:
    '''Class for AMV Signal analysis.'''
    def __init__(self, df, **kwargs):
        # Convert to Polars DataFrame if input is Pandas DataFrame
        if isinstance(df, pd.DataFrame):
            self.df = pl.from_pandas(df)
            self.backend = "pandas"
        elif isinstance(df, pl.DataFrame):
            self.df = df
            self.backend = "polars"
        else:
            raise TypeError("Unsupported dataframe type. Must be pandas.DataFrame or polars.DataFrame.")

        self.parameters = amvParameters(**kwargs)  # Pass kwargs to amvParameters

    def __str__(self):
        """Get a string representation of the dataframe and parameters."""
        return f"Converted to Polars DataFrame, Parameters: {self.parameters.params}"

    # Example analysis methods using Polars functionality
    def get_column_names(self):
        """Retrieve column names."""
        return self.df.columns

    def filter_rows(self, column_name, value, df=None):
        """Filter rows where the column equals a specific value."""
        if df is None:
            self.df_filtered = self.df.filter(pl.col(column_name) == value)
        else: # Filter the passed one
            self.df_filtered = df.filter(pl.col(column_name) == value)
        return self.df_filtered

    def add_column(self, column_name, values):
        """Add a new column to the Polars DataFrame."""
        self.df = self.df.with_columns(pl.Series(column_name, values))
        return self.df
    
    def to_pandas(self):
        """Convert the Polars DataFrame back to Pandas DataFrame if needed."""
        return self.df.to_pandas()

def goal():
    print("This is the goal function.")