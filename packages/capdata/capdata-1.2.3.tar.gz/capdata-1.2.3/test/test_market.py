import unittest
import data.market as market
import pandas


class TestMarketFunctions(unittest.TestCase):
    def test_get_hist_mkt(self):
        market_data = market.get_hist_mkt(['200310.IB', '190008.IB'], '2024-05-09', '2024-05-10 00:00:00',
                                          ['bid', 'ask'],
                                          )
        market_data = pandas.DataFrame(market_data)
        print(market_data)

    def test_get_live_mkt(self):
        market_data = market.get_live_mkt(['200310.IB', '190008.IB'], ['bid', 'ask'],
                                          )
        market_data = pandas.DataFrame(market_data)
        print(market_data)
