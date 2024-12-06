import math
import pandas as pd

from .shiller_header_constants import *


def extract_rolling_windows(df: pd.DataFrame, 
                            length_of_window: int, 
                            window_stride: int,
                            columns_to_rebase: list[str] | None = None):
    subsets: list[pd.DataFrame] = []
    start_index = 0

    while start_index + length_of_window * window_stride <= len(df):
        subset: pd.DataFrame = df.iloc[start_index:start_index + length_of_window * window_stride: window_stride].copy()
        subset.name = df.index[start_index]
        subset.reset_index(drop=True, inplace=True)
        subsets.append(subset)
        start_index += window_stride
    
    if(columns_to_rebase):
        for col in columns_to_rebase:
            if col not in df.columns:
                raise ValueError(f"The column '{col}' does not exist in the DataFrame.")
            for subset in subsets:
                rebase_column(subset, col)
            
    return subsets

def rebase_column(df, column_name):
    """
    Rebase a DataFrame column by dividing every element by the first element of that column.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the column to rebase.
    column_name (str): The name of the column to rebase.
    """
    # Check if the column exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"The column '{column_name}' does not exist in the DataFrame.")
    
    first_value = df[column_name].iloc[0]
    
    if math.isnan(first_value):
        raise ValueError("Cannot rebase on the first value of NaN.")
    if first_value == 0:
        raise ValueError("Cannot rebase on the first value of zero to avoid division by zero.")

    # Rebase the column
    df[column_name] = df[column_name] / first_value

def get_filtered_and_rebased(df, start_date, end_date):
    filtered_df = df.loc[start_date:end_date].copy()

    rebase_column(filtered_df, equities_real_total_return_header)
    rebase_column(filtered_df, bonds_real_total_return_header)
    rebase_column(filtered_df, tbills_real_return_header)
    rebase_column(filtered_df, 'CPI')
    
    return filtered_df

