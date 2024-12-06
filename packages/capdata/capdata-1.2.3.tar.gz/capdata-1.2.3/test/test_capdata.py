import unittest
import capdata


class TestApiFunctions(unittest.TestCase):
    def test_init(self):
        capdata.init("xxxxx", "xxxx")

    def test_get_bond_yield_curve(self):
        curve_data = capdata.get_bond_yield_curve("CN_TREAS_MKT", '2024-05-27 00:00:00', '2024-05-27 18:00:00', 'd',
                                                  True)
        if curve_data is not None:
            for data in curve_data:
                print(data)
        else:
            print(curve_data)

    def test_get_bond_spread_curve(self):
        curve_data = capdata.get_bond_spread_curve("CN_RAILWAY_SPRD_STD", '2024-05-27 00:00:00', '2024-05-27 18:00:00',
                                                   '1m', True)
        if curve_data is not None:
            for data in curve_data:
                print(data)
        else:
            print(curve_data)

    def test_get_ir_yield_curve(self):
        curve_data = capdata.get_ir_yield_curve("CNY_FR_007", '2024-05-22 00:00:00', '2024-05-27 18:00:00', 'd', True)
        if curve_data is not None:
            for data in curve_data:
                print(data)
        else:
            print(curve_data)

    def test_get_dividend_curve(self):
        curve_data = capdata.get_dividend_curve("50ETF_SSE_DIVIDEND", '2024-06-04 00:00:00', '2024-06-06 18:00:00',
                                                'd', True)
        if curve_data is not None:
            for data in curve_data:
                print(data)
        else:
            print(curve_data)

    def test_get_vol_surface(self):
        curve_data = capdata.get_vol_surface("USDCNY_VOL_SVI", '2024-05-10 00:00:00', '2024-06-18 18:00:00', 'd')
        if curve_data is not None:
            for data in curve_data:
                print(data)
        else:
            print(curve_data)

    def test_get_hist_clazz_mkt(self):
        market_data = capdata.get_hist_mkt(['2400004.IB', '2405687.IB'], '2024-09-02', '2024-09-03',
                                           ['bid', 'ask', 'open_ytm'],
                                           freq='d', clazz='BOND')
        print(market_data)

    def test_get_hist_mkt(self):
        market_data = capdata.get_hist_mkt(["200310.IB", "CNY_LPR_5Y_SWAP_10Y", "USDCNY_SPOT", "FR_007",
                                            "CFETS_SHCH_PRIVATE_SECTOR_CDS_INDEX_2Y"],
                                           '2024-09-02', '2024-09-03', ['bid', 'ask', 'open_ytm'], freq='d')
        print(market_data)

    def test_get_live_mkt(self):
        market_data = capdata.get_live_mkt(['200310.IB', '190008.IB'], ['bid', 'ask'],
                                           )
        print(market_data)

    def test_get_pricing(self):
        pricing_data = capdata.get_pricing(['2292030.IB', '2292012.IB'], '2024-05-26', '2024-05-29 00:00:00',
                                           ['duration', 'modified_duration'],
                                           freq='1m')
        if pricing_data is not None:
            for data in pricing_data:
                print(data)
        else:
            print(pricing_data)

    def test_get_valuation(self):
        pricing_data = capdata.get_valuation(['2292030.IB', '2292012.IB'], '2024-05-26', '2024-05-29 00:00:00',
                                             ['present_value', 'dv01', 'cs01'],
                                             freq='1m')
        if pricing_data is not None:
            for data in pricing_data:
                print(data)
        else:
            print(pricing_data)

    def test_get_holidays(self):
        calendar = capdata.get_holidays('CFETS')
        if calendar is not None:
            print(calendar)
        else:
            print(calendar)

    def test_get_sim_bond_yield_curve(self):
        risk_data = capdata.get_sim_bond_yield_curve('CN_TREAS_STD_SIM', '2024-01-05', '2024-01-04', parse_proto=True)
        if risk_data is not None:
            for data in risk_data:
                print(data)
        else:
            print(risk_data)

    def test_get_hist_sim_ir_curve(self):
        risk_data = capdata.get_hist_sim_ir_curve('CN_TREAS_STD', '2024-05-28', '2024-05-27')
        if risk_data is not None:
            for data in risk_data:
                print(data)
        else:
            print(risk_data)

    def test_get_hist_sim_credit_curve(self):
        risk_data = capdata.get_hist_sim_credit_curve('CN_CORP_AAA_SPRD_STD', '2024-05-28', '2024-05-27')
        if risk_data is not None:
            for data in risk_data:
                print(data)
        else:
            print(risk_data)

    def test_get_hist_stressed_ir_curve(self):
        risk_data = capdata.get_hist_stressed_ir_curve('CN_TREAS_PRIME', '2024-05-11', '2024-05-10')
        if risk_data is not None:
            for data in risk_data:
                print(data)
        else:
            print(risk_data)

    def test_get_hist_stressed_credit_curve(self):
        risk_data = capdata.get_hist_stressed_credit_curve('CN_SP_MTN_AAA_SPRD_STD', '2024-05-11', '2024-05-10')
        if risk_data is not None:
            for data in risk_data:
                print(data)
        else:
            print(risk_data)

    def test_get_inst_sim_pnl(self):
        risk_data = capdata.get_inst_sim_pnl(['2171035.IB', '2105288.IB'], '2024-05-28', '2024-05-27')
        if risk_data is not None:
            for data in risk_data:
                print(data)
        else:
            print(risk_data)

    def test_get_inst_stressed_pnl(self):
        risk_data = capdata.get_inst_stressed_pnl(['2171035.IB', '2105288.IB'], '2024-05-28', '2024-05-27')
        if risk_data is not None:
            for data in risk_data:
                print(data)
        else:
            print(risk_data)

    def test_get_inst_var(self):
        risk_data = capdata.get_inst_var("2171035.IB", '2024-05-28', '2024-05-27', ['var', 'es'])
        if risk_data is not None:
            print(risk_data)
        else:
            print(risk_data)

    def test_get_ir_index(self):
        ir_index_data = capdata.get_ir_index(['CNY'])
        if ir_index_data is not None:
            for data in ir_index_data:
                print(data)
        else:
            print(ir_index_data)

    def test_get_ir_definition(self):
        datas = capdata.get_ir_index_definition(['FR_001'])
        if datas is not None:
            for data in datas:
                print(data)
        else:
            print(datas)

    def test_get_ir_curve_list(self):
        datas = capdata.get_ir_curve_list(['CNY'], ['FR_007'])
        if datas is not None:
            for data in datas:
                print(data)
        else:
            print(datas)

    def test_get_ir_curve_definition(self):
        datas = capdata.get_ir_curve_definition(['CNY_FR_007'])
        if datas is not None:
            for data in datas:
                print(data)
        else:
            print(datas)

    def test_get_bond_yield_curve_list(self):
        datas = capdata.get_bond_yield_curve_list(['CNY'], [])
        if datas is not None:
            for data in datas:
                print(data)
        else:
            print(datas)

    def test_get_std_bond_yield_curve_list(self):
        datas = capdata.get_std_bond_yield_curve_list(['CNY'], [])
        if datas is not None:
            for data in datas:
                print(data)
        else:
            print(datas)

    def test_get_bond_yield_curve_definition(self):
        datas = capdata.get_bond_yield_curve_definition(['CN_RAILWAY_MKT'])
        if datas is not None:
            for data in datas:
                print(data)
        else:
            print(datas)

    def test_get_bond_credit_curve_list(self):
        datas = capdata.get_bond_credit_curve_list(['CNY'], [])
        if datas is not None:
            for data in datas:
                print(data)
        else:
            print(datas)

    def test_get_std_bond_credit_curve_list(self):
        datas = capdata.get_std_bond_credit_curve_list(['CNY'], [])
        if datas is not None:
            for data in datas:
                print(data)
        else:
            print(datas)

    def test_get_bond_credit_curve_definition(self):
        datas = capdata.get_bond_credit_curve_definition(['CN_SP_MTN_AA+_SPRD_STD'])
        if datas is not None:
            for data in datas:
                print(data)
        else:
            print(datas)

    def test_get_bond_list(self):
        datas = capdata.get_bond_list(['CFETS'], ['CNY'], ['国债'], ['FIXED_COUPON_BOND'], [])
        if datas is not None:
            for data in datas:
                print(data)
        else:
            print(datas)

    def test_get_std_bond_list(self):
        datas = capdata.get_std_bond_list(['CNY'], ['TREASURY_BOND'], ['FIXED_COUPON_BOND'], [])
        if datas is not None:
            for data in datas:
                print(data)
        else:
            print(datas)

    def test_get_bond_definition(self):
        datas = capdata.get_bond_definition(['050220.IB'])
        if datas is not None:
            for data in datas:
                print(data)
        else:
            print(datas)

    def test_get_bond_pricing_settings(self):
        datas = capdata.get_bond_pricing_settings(['050220.IB'])
        if datas is not None:
            for data in datas:
                print(data)
        else:
            print(datas)

    def test_get_bond_valuation_settings(self):
        datas = capdata.get_bond_valuation_settings(['050220.IB'])
        if datas is not None:
            for data in datas:
                print(data)
        else:
            print(datas)

    def test_get_bond_sim_valuation_settings(self):
        datas = capdata.get_bond_sim_valuation_settings(['050220.IB'])
        if datas is not None:
            for data in datas:
                print(data)
        else:
            print(datas)

    def test_get_risk_factor_definition(self):
        datas = capdata.get_risk_factor_definition(['RF_CN_TREAS_ZERO_1M'])
        if datas is not None:
            for data in datas:
                print(data)
        else:
            print(datas)

    def test_get_risk_factor_group_definition(self):
        datas = capdata.get_risk_factor_group_definition(['FI_BOND_IR_CN_IB_HIST_SIM_SCN_GROUP'])
        if datas is not None:
            for data in datas:
                print(data)
        else:
            print(datas)

    def test_get_ir_vanilla_instrument_definition(self):
        datas = capdata.get_ir_vanilla_instrument_definition(
            ['CNY_CNHHIBOR_DEPO_12M', 'CNY_LPR_5Y_SWAP_7Y', 'SHIBOR_USDLIBOR_3M_SWAP_1Y'])
        print(datas)

    def test_get_ir_vanilla_swap_list(self):
        datas = capdata.get_ir_vanilla_swap_list(ccy=['CNY'], ir_index=['FR_007'])
        print(datas)

    def test_get_ir_depo_list(self):
        datas = capdata.get_ir_depo_list(['CNY'])
        print(datas)

    def test_get_xccy_swap_list(self):
        datas = capdata.get_xccy_swap_list(ccy=['CNY'], ir_index=['USDLIBOR_3M'])
        print(datas)
