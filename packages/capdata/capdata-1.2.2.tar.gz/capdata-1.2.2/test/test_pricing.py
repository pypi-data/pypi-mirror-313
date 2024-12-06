import unittest
import data.pricing as pricing


class TestPricingFunctions(unittest.TestCase):
    def test_get_pricing(self):
        pricing_data = pricing.get_pricing(['2292030.IB', '2292012.IB'], '2024-05-26', '2024-05-29 00:00:00',
                                           ['duration', 'modified_duration'],
                                           freq='1m')
        if pricing_data is not None:
            for data in pricing_data:
                print(data)
        else:
            print(pricing_data)

    def test_get_valuation(self):
        pricing_data = pricing.get_valuation(['2292030.IB', '2292012.IB'], '2024-05-26', '2024-05-29 00:00:00',
                                             ['present_value', 'dv01', 'cs01'],
                                             freq='1m')
        if pricing_data is not None:
            for data in pricing_data:
                print(data)
        else:
            print(pricing_data)
