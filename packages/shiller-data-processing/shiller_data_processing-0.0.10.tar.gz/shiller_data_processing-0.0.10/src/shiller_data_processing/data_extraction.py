import pandas as pd
import numpy as np

from .shiller_header_constants import *
from .dataframe_manipulations import rebase_column

def read_simba_tbills_data(simba_tbills_data_location: str, cpi_data: pd.DataFrame):
    raw_tbills_column_name = 'TBills (no fee)'
    raw_year_column_name = 'Year'
    df_tbills = pd.read_excel(simba_tbills_data_location, engine='odf') 
    
    #remove first row as don't have CPI coverage to convert to real return
    df_tbills = df_tbills.drop(index=0)
    df_tbills = df_tbills.reset_index(drop=True)
    
    df_tbills[tbills_total_return_header] = (1 + df_tbills[raw_tbills_column_name]/100).cumprod()
    df_tbills.loc[-1] = [1871,np.nan, 1]  # adding a row
    df_tbills.index = df_tbills.index + 1  # shifting index
    df_tbills = df_tbills.sort_index()  # sorting by index
    df_tbills = df_tbills.drop(columns=raw_tbills_column_name)
    
    df_tbills['Date'] = pd.to_datetime(df_tbills[raw_year_column_name], format='%Y') + pd.DateOffset(months=11, days=30)
    df_tbills = df_tbills.drop(columns=raw_year_column_name)
    df_tbills.set_index('Date', inplace=True)
    
    base_date = df_tbills.index[0]
    base_cpi = cpi_data.loc[base_date, 'CPI']
    
    
    def calculate_real_return(row):
        current_date = row.name
        current_cpi = _get_cpi(cpi_data, current_date)
        inflation_rate = current_cpi / base_cpi
        real_return = row[tbills_total_return_header] / inflation_rate
        return real_return
    
    df_tbills[tbills_real_return_header] = df_tbills.apply(calculate_real_return, axis=1)
    df_tbills = df_tbills.drop(columns=tbills_total_return_header)
    
    min_tbills_date = base_date
    
    return (df_tbills, min_tbills_date)

def read_shiller_data(shiller_data_location):
    df_raw = pd.read_excel(shiller_data_location, sheet_name='Data')

    real_total_return_price_col = 9
    real_earnings_col = 10
    CPI_col = 4
    CAPE_col = 12
    real_total_bond_returns_col = 18
    ten_year_treasury_yield_col = 6    

    _validate_sheet(df_raw, real_earnings_col, CPI_col, ten_year_treasury_yield_col)
    min_date = pd.Timestamp('1871-01-31')

    df_selected = df_raw.iloc[:, [real_total_return_price_col, real_earnings_col, CPI_col, CAPE_col, 
                                  real_total_bond_returns_col, ten_year_treasury_yield_col]]

    df_trimmed = df_selected.iloc[7:] 

    df_trimmed.columns = [equities_real_total_return_header, 'Real earnings', 'CPI', 'CAPE', 
                          bonds_real_total_return_header, ten_year_treasury_yield_header]

    # Remove the last row if it contains NaN
    if df_trimmed.tail(1).isna().any(axis=1).item():
        df_trimmed = df_trimmed.iloc[:-1]

    #remove last row as it's a partial month
    df_trimmed = df_trimmed.iloc[:-1]

    # Reset the index (since rows were removed)
    df_trimmed.reset_index(drop=True, inplace=True)

    rebase_column(df_trimmed, equities_real_total_return_header)

    if not df_trimmed.loc[0, bonds_real_total_return_header] == 1:
        raise AssertionError("Bond TRs need rebasing.")

    dates = pd.date_range(start=min_date, periods=len(df_trimmed), freq='ME')
    df_trimmed.insert(0, 'Date', dates)
    df_trimmed.set_index('Date', inplace=True)
    
    return (df_trimmed, min_date)

def _validate_sheet(df_raw, real_earnings_col, CPI_col, ten_year_treasury_yield_col):
    stock_data_header_correct = (
        df_raw.iloc[3, 9] == "Real" and
        df_raw.iloc[4, 9] == "Total" and
        df_raw.iloc[5, 9] == "Return" and
        df_raw.iloc[6, 9] == "Price"
    )

    bond_data_header_correct = (
        df_raw.iloc[3, 18] == "Real" and
        df_raw.iloc[4, 18] == "Total" and
        df_raw.iloc[5, 18] == "Bond" and
        df_raw.iloc[6, 18] == "Returns"
    )

    cape_header_correct = df_raw.iloc[6, 12] == "CAPE"
    real_earnings_header_correct = (
        df_raw.iloc[5, real_earnings_col] == "Real" and
        df_raw.iloc[6, real_earnings_col] == "Earnings"
    )
    cpi_header_correct = df_raw.iloc[6, CPI_col] == "CPI"
    ten_year_treasury_yields_header_correct = df_raw.iloc[6, ten_year_treasury_yield_col] == "Rate GS10"

    if (not stock_data_header_correct 
        or not bond_data_header_correct 
        or not cape_header_correct
        or not real_earnings_header_correct
        or not cpi_header_correct
        or not ten_year_treasury_yields_header_correct):
        raise AssertionError("Data doesn't line up as expected.")
    
    first_date = df_raw.iloc[7, 0]    
    if(str(first_date) != '1871.01'): raise AssertionError("Data doesn't line up as expected.")

def _get_cpi(cpi_data, date: np.datetime64):
    return cpi_data.loc[date, 'CPI']