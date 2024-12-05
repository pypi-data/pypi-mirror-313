import pandas as pd
import numpy as np
import inspect
import matplotlib.pyplot as plt
import seaborn as sns
import shutil


class Statistics:
    def get_leading_zeros(self, df):
        lz_cols = {}

        # Select only object and string columns
        string_cols = df.select_dtypes(include=["object", "string"]).columns

        for col in string_cols:
            # Filter rows where the specified column has leading zeros
            filtered_df = df[df[col].astype(str).fillna("").str.startswith("0")]

            # Check if there are any matching rows
            if not filtered_df.empty:
                # Extract all matching values and format them
                leading_zero_values = filtered_df[
                    col
                ].unique()  # Get unique values with leading zeros
                lz_cols[col] = (
                    leading_zero_values.tolist()
                )  # Convert to list for easier readability

        # Balancing df by column lengths
        max_length = max(len(v) for v in lz_cols.values()) if lz_cols else 0
        for key in lz_cols.keys():
            while len(lz_cols[key]) < max_length:
                lz_cols[key].append(None)  # Fill shorter lists with None

        return pd.DataFrame(lz_cols)  # Return the DataFrame of leading zeros

    def get_outliers(self, series):
        """Identify outliers in a Series using the IQR method."""
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        return (series < lower_bound) | (series > upper_bound)

    def get_str_stats(self, stats_data, df, col):
        # Get strings data
        unique_dtypes = df[col].apply(type).unique()
        dtype_str = ", ".join([dtype.__name__ for dtype in unique_dtypes])
        stats_data["DTypes"].append(dtype_str)
        stats_data["NaNs"].append(df[col].isna().sum())
        stats_data["0_values"].append((df[col] == 0).sum())
        stats_data["Unique"].append(len(df[col].unique()))
        stats_data["Duplicates"].append(df[col].duplicated().sum())

    def get_float_stats(self, stats_data, df, col):
        # Check if the column is numeric and calculate stats accordingly
        if pd.api.types.is_numeric_dtype(df[col]):
            # Convert to floats
            df[col] = df[col].fillna(0).astype(float)
            # Calculate statistics
            stats_data["Min"].append(df[col].min())
            stats_data["Max"].append(df[col].max())
            stats_data["Mean"].append(df[col].mean())
            stats_data["Median"].append(df[col].median())
            stats_data["STD"].append(df[col].std())
            stats_data["STD (%)"].append(
                (df[col].std() / df[col].mean()) * 100
                if df[col].mean() != 0
                else np.nan
            )
            stats_data["Totals"].append(df[col].sum())

            # Use the get_outliers function to determine outliers
            stats_data["Outliers"].append(self.get_outliers(df[col]).sum())

        else:
            # If not numeric, append NaN for numeric statistics
            for key in [
                "Min",
                "Max",
                "Mean",
                "Median",
                "STD",
                "STD (%)",
                "Outliers",
                "Totals",
            ]:
                stats_data[key].append(np.nan)

    def get_stats(self, df):
        """Calculate various statistics for the DataFrame."""
        stats_data = {
            "DTypes": [],
            "NaNs": [],
            "0_values": [],
            "Unique": [],
            "Duplicates": [],
            "Totals": [],
            "Min": [],
            "Max": [],
            "Mean": [],
            "Median": [],
            "STD": [],
            "STD (%)": [],
            "Outliers": [],
        }

        # Building statistics table by a col
        for col in df.columns:
            self.get_str_stats(stats_data, df, col)
            self.get_float_stats(stats_data, df, col)

        # Create a DataFrame from the collected statistics at once
        return pd.DataFrame(stats_data, index=df.columns), len(df)

    def show_stats(self, df):
        # Setting display params
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", 1000)
        pd.set_option("display.max_colwidth", 30)
        pd.set_option("display.float_format", "{:,.2f}".format)

        """Display Data Frame name """
        frame = inspect.currentframe()
        try:
            local_vars = frame.f_back.f_locals
            df_name = [name for name, value in local_vars.items() if value is df]
            df_name = df_name[0] if df_name else "DataFrame"
        finally:
            del frame

        lz = self.get_leading_zeros(df)
        stats, length_of_df = self.get_stats(df)

        # Get the current terminal size
        screen_width = shutil.get_terminal_size().columns
        print(f"{'=' * screen_width} {df_name} {'=' * screen_width}")

        print("\nLeading zeros in columns\n")
        print(lz.head(3))

        print("\nGeneral stats\n")
        print(stats)

        print(f"Overall data frame length: {length_of_df}")

    def show_sctplot(self, df, col):
        """Create scatter plots for each column with outliers."""

        plt.figure(figsize=(10, 6))

        outliers = self.get_outliers(df[col])

        sns.scatterplot(
            data=df,
            x=df.index,
            y=df[col],
            hue=outliers,
            palette={True: "red", False: "blue"},
            legend=False,
        )

        plt.title(f"{col}")
        plt.xlabel("rows")
        plt.ylabel(col)

        plt.axhline(y=df[col].mean(), color="green", linestyle="--", label="Mean")
        plt.axhline(y=df[col].median(), color="orange", linestyle="--", label="Median")

        plt.legend()

        plt.tight_layout()

        plt.show()


# Module-level functions that users can call directly
def show_stats(df):
    """Display statistics for the given DataFrame."""
    stats_instance = Statistics()  # Create an instance of Statistics
    return stats_instance.show_stats(df)


def show_sctplot(df, col):
    """Display a scatter plot for the specified column in the DataFrame."""
    stats_instance = Statistics()  # Create an instance of Statistics
    return stats_instance.show_sctplot(df, col)
