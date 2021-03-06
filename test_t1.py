import datetime
import unittest
from t1 import Stocks
from freezegun import freeze_time


class StocksTestCase(unittest.TestCase):
    def setUp(self):
        self.stocks = Stocks()

    def test_loaded_data(self):
        """Test if the number of rows of data loaded is correct"""
        self.assertEqual(self.stocks.stocks_df.shape[0], 5)

    def test_dividend_yield(self):
        """Test if the dividend yield calculation is correct"""
        self.assertEqual(self.stocks.get_dividend_yield('POP', 100), 0.08)

    def test_p_e_ratio_success(self):
        """Test if the get_p_e_ratio calculation is correct
        on success """
        self.assertEqual(self.stocks.get_p_e_ratio('ALE', 69), 3)

    def test_p_e_ratio_failure(self):
        """Test if the get_p_e_ratio behaviour is correct on failure"""
        self.assertEqual(self.stocks.get_p_e_ratio('TEA', 100), -1)

    def test_trade(self):
        """Test the trading mechanism stock_trade"""
        # Note: A slightly older version of Pandas is used since
        # the current freezegun version is incompatible with current pandas version
        current_date_time = datetime.datetime.now()
        with freeze_time(current_date_time):
            self.stocks.stock_trade('POP', 10, 'buy', 100)
            self.assertEqual(self.stocks.trades_df.shape[0], 1)
            trade_data = {'StockSymbol': 'POP',
                          'Timestamp': datetime.datetime.now(),
                          'Quantity': 10,
                          'Buy_Sell': 'buy',
                          'Price': 100}
            trade_data_retrieved = self.stocks.trades_df.iloc[[0],
                                                              [0, 1, 2, 3, 4]].to_dict()
            trade_data_dict = {key: value[0] for key, value in
                               trade_data_retrieved.items()}
            self.assertEqual(trade_data_dict, trade_data)

    def test_weighted_stock_price(self):
        """Test the weighted stock price calculation function calc_weighted_stock_price"""
        with freeze_time('2000-1-1'):
            # this trade should not be taken into account
            # since earlier than 15 minutes
            self.stocks.stock_trade('POP', 100, 'buy', 500)

        self.stocks.stock_trade('POP', 50, 'buy', 100)
        self.stocks.stock_trade('POP', 50, 'buy', 200)
        current_date_time = datetime.datetime.now()
        weighted_stock_price = self.stocks.calc_weighted_stock_price('POP',
                                                                     current_date_time)
        self.assertEqual(weighted_stock_price, 150)

    def test_share_index(self):
        """Test the share index calculation function calc_share_index"""
        self.stocks.stock_trade('POP', 50, 'buy', 100)
        self.stocks.stock_trade('TEA', 10, 'buy', 110)
        self.stocks.stock_trade('ALE', 20, 'buy', 500)
        self.stocks.stock_trade('POP', 3, 'buy', 300)
        self.stocks.stock_trade('GIN', 15, 'buy', 327.56)
        self.stocks.stock_trade('JOE', 500, 'buy', 201.51)
        share_index = self.stocks.calc_share_index()
        self.assertEqual(share_index, 255.51375357750982)







