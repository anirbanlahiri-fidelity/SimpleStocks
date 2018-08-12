import pandas as pd
import numpy as np
import datetime

# df = pd.DataFrame(np.random.randn(5,5),
#         columns=['StockSymbol', 'Type', 'LastDividend', 'FixedDividend', 'ParValue'])


class Stocks:

    def __init__(self):
        self.stocks_df = pd.read_csv('data.csv')
        self.stocks_df.set_index('StockSymbol', inplace=True)
        self.trades_df = pd.DataFrame(columns=['StockSymbol', 'Timestamp', 'Quantity',
                                               'Buy_Sell', 'Price'])
        # self.vwap = pd.DataFrame(columns=['StockSymbol', 'Timestamp')
        # self.trades_df.set_index('StockSymbol', inplace=True)
        # print(self.stocks_df)
        # return df

    def get_dividend_yield(self, stock_symbol, market_price):
        # print(list(df))
        # print(df.loc[StockSymbol][1])
        # print(df.loc[(StockSymbol, 'LastDividend')])
        # print(self.stocks_df.loc[stock_symbol]['LastDividend'])
        # last_dividend = data_frame.loc[stock_symbol]['LastDividend']
        try:
            if self.stocks_df.loc[stock_symbol]['Type'] == 'Common':
                dividend_yield = self.stocks_df.loc[stock_symbol]['LastDividend'] / \
                                 market_price
            else:
                dividend_yield = self.stocks_df.loc[stock_symbol]['FixedDividend'] / \
                                 market_price
        except ZeroDivisionError:
            print("Market Price is zero!")
        return dividend_yield

    def get_p_e_ratio(self, stock_symbol, market_price):
        if self.stocks_df.loc[stock_symbol]['LastDividend'] == 0:
            # Assuming -1 is returned if the P/E ratio cannot be calculated
            return -1
        else:
            return market_price/self.stocks_df.loc[stock_symbol]['LastDividend']

    def stock_trade(self, stock_symbol, stock_quantity, buy_sell, trade_price):
        self.trades_df = self.trades_df.append({'StockSymbol': stock_symbol,
                                                'Timestamp': datetime.datetime.now(),
                                                'Quantity': stock_quantity,
                                                'Buy_Sell': buy_sell,
                                                'Price': trade_price}, ignore_index=True)
        print(self.trades_df)

    def calc_weighted_stock_price(self, stock_symbol, current_time):
        total_volume = 0
        volume_weighted_total = 0
        for index, row in self.trades_df.iterrows():
            time_elapsed = current_time - row['Timestamp']
            if (stock_symbol == row['StockSymbol']) and \
                    (time_elapsed < datetime.timedelta(minutes=15)):
                # update the totals
                total_volume += row['Quantity']
                volume_weighted_total += row['Quantity'] * row['Price']
        if total_volume == 0:
            # assuming that there were no trades in the last 15 minutes
            # then weighted average is 0
            return 0
        else:
            return volume_weighted_total / total_volume

    def show_stocks(self):
        print(self.stocks_df)

    def show_trades(self):
        print(self.trades_df)

    # def load_data(self):
    #     # df = pd.DataFrame(columns=['StockSymbol', 'Type', 'LastDividend', 'FixedDividend', 'ParValue'])
    #     df = pd.read_csv('data.csv')
    #     df.set_index('StockSymbol', inplace=True)
    #     return df


if __name__ == "__main__":
    stocks = Stocks()
    stocks.show_stocks()
    print('Dividend yield : ', stocks.get_dividend_yield('POP', 100))
