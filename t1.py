import pandas as pd
import numpy as np

# df = pd.DataFrame(np.random.randn(5,5),
#         columns=['StockSymbol', 'Type', 'LastDividend', 'FixedDividend', 'ParValue'])


def get_dividend_yield(data_frame, stock_symbol, market_price):
    # print(list(df))
    # print(df.loc[StockSymbol][1])
    # print(df.loc[(StockSymbol, 'LastDividend')])
    print(data_frame.loc[stock_symbol]['LastDividend'])
    # last_dividend = data_frame.loc[stock_symbol]['LastDividend']
    try:
        if data_frame.loc[stock_symbol]['Type'] == 'Common':
            dividend_yield = data_frame.loc[stock_symbol]['LastDividend'] / market_price
        else:
            dividend_yield = data_frame.loc[stock_symbol]['FixedDividend'] / market_price
    except ZeroDivisionError:
        print("Market Price is zero!")
    return dividend_yield


def get_p_e_ratio(data_frame, stock_symbol, market_price):
    if data_frame.loc[stock_symbol]['LastDividend'] == 0:
        # Assuming -1 is returned if the P/E ratio cannot be calculated
        return -1
    else:
        return market_price/data_frame.loc[stock_symbol]['LastDividend']


def stock_trade(stock_symbol, stock_quantity, buy_sell, trade_price):

    pass



def load_data():
    # df = pd.DataFrame(columns=['StockSymbol', 'Type', 'LastDividend', 'FixedDividend', 'ParValue'])
    df = pd.read_csv('data.csv')
    df.set_index('StockSymbol', inplace=True)
    return df


if __name__ == "__main__":
    df = load_data()
    print(df)
    print('Dividend yield : ', get_dividend_yield(df, 'POP', 100))
