import yfinance as yf
import pandas as pd

def get_symbols(region='us', sector='Technology', peer_group='Software & Services'):
    # Get software & services tickers from Yahoo Finance
    query = yf.EquityQuery('and',[
    yf.EquityQuery('EQ',['region', region]),
    yf.EquityQuery('EQ',['sector', sector]),
    yf.EquityQuery('EQ',['peer_group', peer_group])
    ])

    offset = 0
    size = 250
    res = yf.screen(query=query, offset=0, size=250, sortAsc=True)
    df_symbols = pd.DataFrame(res['quotes'])[['symbol','shortName']]

    if res['total'] > size:
        for i in range(res['total']//size):
            offset += size
            res = yf.screen(query=query, offset=offset, size=size, sortAsc=True)
            df_symbols = pd.concat([df_symbols, pd.DataFrame(res['quotes'])[['symbol','shortName']]])

    df_symbols.reset_index(drop=True, inplace=True) 
    return df_symbols
