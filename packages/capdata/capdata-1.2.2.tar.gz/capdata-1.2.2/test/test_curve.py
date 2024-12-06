import unittest

import data.curve as curve


class TestCurveFunctions(unittest.TestCase):
    def test_get_bond_curve(self):
        curve_data = curve.get_bond_yield_curve("CN_TREAS_STD", '2024-05-27 00:00:00', '2024-05-27 18:00:00', '1m',
                                                parse_proto=True)
        if curve_data is not None:
            for data in curve_data:
                print(data)
        else:
            print(curve_data)

    def test_get_credit_curve(self):
        curve_data = curve.get_bond_spread_curve("CN_RAILWAY_SPRD_STD", '2024-05-27 00:00:00', '2024-05-27 18:00:00',
                                                 '1m', parse_proto=True)
        if curve_data is not None:
            for data in curve_data:
                print(data)
        else:
            print(curve_data)

    def test_get_ir_yield_curve(self):
        curve_data = curve.get_ir_yield_curve("CNY_FR_007", '2024-05-22 00:00:00', '2024-05-27 18:00:00', 'd',
                                              parse_proto=True)
        if curve_data is not None:
            for data in curve_data:
                print(data)
        else:
            print(curve_data)

    def test_get_dividend_curve(self):
        curve_data = curve.get_dividend_curve("50ETF_SSE_DIVIDEND", '2024-06-04 00:00:00', '2024-06-06 18:00:00', 'd',
                                              parse_proto=True)
        if curve_data is not None:
            for data in curve_data:
                print(data)
        else:
            print(curve_data)

    def test_get_vol_surface(self):
        curve_data = curve.get_vol_surface("USDCNY_VOL_SVI", '2024-06-16 00:00:00', '2024-06-18 18:00:00', 'd')
        if curve_data is not None:
            for data in curve_data:
                print(data)
        else:
            print(curve_data)
