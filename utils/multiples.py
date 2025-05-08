import yfinance as yf
import pandas as pd

# Function to get financial data
def get_financial_data(symbol, freq='Q'):
    stock = yf.Ticker(symbol)
    
    # Get financial statements
    if freq == 'Q':
        balance_sheet = stock.quarterly_balance_sheet
        income_stmt = stock.quarterly_income_stmt
        cash_flow = stock.quarterly_cashflow
    elif freq == 'Y':
        balance_sheet = stock.balance_sheet
        income_stmt = stock.income_stmt
        cash_flow = stock.cashflow
    else:
        raise ValueError(f"Invalid frequency: {freq}")
    
    return {
        'balance_sheet': balance_sheet,
        'income_stmt': income_stmt,
        'cash_flow': cash_flow
    }


def get_valuation_multiples(symbol, multiple_types):
    def safe_get(info_dict, key):
        try:
            result = info_dict.get(key)
            if result is None:
                print(f"Warning: {key} returned None")
            return result
        except:
            print(f"Error getting {key}")
            return None
            
    def safe_ratio(info_dict, numerator_key, denominator_key):
        try:
            numerator = safe_get(info_dict, numerator_key)
            denominator = safe_get(info_dict, denominator_key)
            if numerator is None or denominator is None:
                print(f"Warning: Could not calculate ratio {numerator_key}/{denominator_key} - numerator or denominator is None")
                return None
            if denominator == 0:
                print(f"Warning: Could not calculate ratio {numerator_key}/{denominator_key} - denominator is 0")
                return None
            return numerator / denominator
        except:
            print(f"Error calculating ratio {numerator_key}/{denominator_key}")
            return None

    # Get info and initialize multiples dict
    info = yf.Ticker(symbol).info
    multiples = {}

    for multiple_type in multiple_types:
        if multiple_type == 'PER':
            multiples[multiple_type] = safe_get(info, 'trailingPE')
        elif multiple_type == 'PBR':
            multiples[multiple_type] = safe_get(info, 'priceToBook')
        elif multiple_type == 'EV/Revenue':
            multiples[multiple_type] = safe_get(info, 'enterpriseToRevenue')
        elif multiple_type == 'EV/EBITDA':
            multiples[multiple_type] = safe_get(info, 'enterpriseToEbitda')
        elif multiple_type == 'PEG':
            multiples[multiple_type] = safe_get(info, 'trailingPegRatio')
        elif multiple_type == 'Profit Margin':
            multiples[multiple_type] = safe_get(info, 'profitMargins')
        elif multiple_type == 'Operating Margin':
            multiples[multiple_type] = safe_get(info, 'operatingMargins')
        elif multiple_type == 'ROA':
            multiples[multiple_type] = safe_get(info, 'returnOnAssets')
        elif multiple_type == 'ROE':
            multiples[multiple_type] = safe_get(info, 'returnOnEquity')
        elif multiple_type == 'Beta':
            multiples[multiple_type] = safe_get(info, 'beta')
        elif multiple_type == 'Debt/Equity':
            multiples[multiple_type] = safe_get(info, 'debtToEquity')
        elif multiple_type == 'Cash/Revenue':
            multiples[multiple_type] = safe_ratio(info, 'totalCash', 'totalRevenue')
        elif multiple_type == 'Debt/Revenue':
            multiples[multiple_type] = safe_ratio(info, 'totalDebt', 'totalRevenue')

    return multiples

def get_valuation_multiples_for_symbols(df_symbols, multiple_types=None):
    """
    symbols: pd.DataFrame with columns ['symbol', 'shortName']
    multiple_types: list of multiple types to calculate
    - PER: Price to Earnings Ratio
    - PBR: Price to Book Ratio
    - EV/Revenue: Enterprise Value to Revenue
    - EV/EBITDA: Enterprise Value to EBITDA
    - PEG: Price to Earnings Growth Ratio
    - Profit Margin: Profit Margin
    - Operating Margin: Operating Margin
    - ROA: Return on Assets
    - ROE: Return on Equity
    - Beta: Beta
    - Debt/Equity: Debt to Equity
    - Cash/Revenue: Cash to Revenue
    - Debt/Revenue: Debt to Revenue
    """
    # Create empty list to store results
    results = []
    if multiple_types is None:
        multiple_types = ['PER', 'PBR', 'EV/Revenue', 'EV/EBITDA', 'PEG', 'Profit Margin', 'Operating Margin', 'ROA', 'ROE', 'Beta', 'Debt/Equity', 'Cash/Revenue', 'Debt/Revenue']

    # Iterate through each symbol
    for idx, row in df_symbols.iterrows():
    # Get valuation multiples for current symbol
        multiples = get_valuation_multiples(row['symbol'], multiple_types)
        
        # Combine symbol, shortname and multiples into dict
        result_dict = {
            'symbol': row['symbol'],
            'shortName': row['shortName']
        }
        result_dict.update(multiples)
        
        # Append to results list
        results.append(result_dict)
        
        # Print progress
        print(f"Processed {idx+1}/{len(df_symbols)} symbols")

    # Create dataframe from results
    df_results = pd.DataFrame(results)
    return df_results