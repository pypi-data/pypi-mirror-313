import unittest
import data.refer as refer


class TestReferFunctions(unittest.TestCase):
    def test_get_holidays(self):
        calendar = refer.get_holidays('CFETS')
        if calendar is not None:
            print(calendar)
        else:
            print(calendar)

    def test_get_ir_index(self):
        ir_index_data = refer.get_ir_index(['CNY'])
        if ir_index_data is not None:
            for data in ir_index_data:
                print(data)
        else:
            print(ir_index_data)

    def test_get_ir_definition(self):
        ir_index_data = refer.get_ir_index_definition(['FR_001'])
        if ir_index_data is not None:
            for data in ir_index_data:
                print(data)
        else:
            print(ir_index_data)

    def test_get_ir_curve_list(self):
        ir_index_data = refer.get_ir_curve_list(['CNY'], ['FR_007'])
        if ir_index_data is not None:
            for data in ir_index_data:
                print(data)
        else:
            print(ir_index_data)

    def test_get_ir_curve_definition(self):
        ir_index_data = refer.get_ir_curve_definition(['CNY_FR_007'])
        if ir_index_data is not None:
            for data in ir_index_data:
                print(data)
        else:
            print(ir_index_data)

    def test_get_bond_yield_curve_list(self):
        ir_index_data = refer.get_bond_yield_curve_list(['CNY'], [], 'MKT')
        if ir_index_data is not None:
            for data in ir_index_data:
                print(data)
        else:
            print(ir_index_data)

    def test_get_bond_yield_curve_definition(self):
        ir_index_data = refer.get_bond_yield_curve_definition(['CN_RAILWAY_MKT'])
        if ir_index_data is not None:
            for data in ir_index_data:
                print(data)
        else:
            print(ir_index_data)

    def test_get_bond_credit_curve_list(self):
        ir_index_data = refer.get_bond_credit_curve_list(['CNY'], [], 'MKT')
        if ir_index_data is not None:
            for data in ir_index_data:
                print(data)
        else:
            print(ir_index_data)

    def test_get_bond_credit_curve_definition(self):
        ir_index_data = refer.get_bond_credit_curve_definition(['CN_SP_MTN_AA+_SPRD_STD'])
        if ir_index_data is not None:
            for data in ir_index_data:
                print(data)
        else:
            print(ir_index_data)

    def test_get_bond_list(self):
        ir_index_data = refer.get_bond_list(['CN_INTER_BANK'], ['CNY'], ['TREASURY_BOND'], ['FIXED_COUPON_BOND'], [],
                                            False)
        if ir_index_data is not None:
            for data in ir_index_data:
                print(data)
        else:
            print(ir_index_data)

    def test_get_bond_definition(self):
        ir_index_data = refer.get_bond_definition(['050220.IB'])
        if ir_index_data is not None:
            for data in ir_index_data:
                print(data)
        else:
            print(ir_index_data)

    def test_get_bond_pricing_settings(self):
        ir_index_data = refer.get_bond_pricing_settings(['050220.IB'])
        if ir_index_data is not None:
            for data in ir_index_data:
                print(data)
        else:
            print(ir_index_data)

    def test_get_bond_valuation_settings(self):
        ir_index_data = refer.get_bond_valuation_settings(['050220.IB'])
        if ir_index_data is not None:
            for data in ir_index_data:
                print(data)
        else:
            print(ir_index_data)

    def test_get_bond_sim_valuation_settings(self):
        ir_index_data = refer.get_bond_sim_valuation_settings(['050220.IB'])
        if ir_index_data is not None:
            for data in ir_index_data:
                print(data)
        else:
            print(ir_index_data)

    def test_get_risk_factor_definition(self):
        ir_index_data = refer.get_risk_factor_definition(['RF_CN_TREAS_ZERO_1M'])
        if ir_index_data is not None:
            for data in ir_index_data:
                print(data)
        else:
            print(ir_index_data)

    def test_get_risk_factor_group_definition(self):
        ir_index_data = refer.get_risk_factor_group_definition(['FI_BOND_IR_CN_IB_HIST_SIM_SCN_GROUP'])
        if ir_index_data is not None:
            for data in ir_index_data:
                print(data)
        else:
            print(ir_index_data)
