import unittest
import data.risk as risk


class TestRiskFunctions(unittest.TestCase):
    def test_get_hist_sim_ir_curve(self):
        risk_data = risk.get_hist_sim_ir_curve('CN_TREAS_STD', '2024-05-28', '2024-05-27')
        if risk_data is not None:
            for data in risk_data:
                print(data)
        else:
            print(risk_data)

    def test_get_hist_sim_credit_curve(self):
        risk_data = risk.get_hist_sim_credit_curve('CN_CORP_AAA_SPRD_STD', '2024-05-28', '2024-05-27')
        if risk_data is not None:
            for data in risk_data:
                print(data)
        else:
            print(risk_data)

    def test_get_hist_stressed_ir_curve(self):
        risk_data = risk.get_hist_stressed_ir_curve('CN_TREAS_PRIME', '2024-05-11', '2024-05-10')
        if risk_data is not None:
            for data in risk_data:
                print(data)
        else:
            print(risk_data)

    def test_get_hist_stressed_credit_curve(self):
        risk_data = risk.get_hist_stressed_credit_curve('CN_SP_MTN_AAA_SPRD_STD', '2024-05-11', '2024-05-10')
        if risk_data is not None:
            for data in risk_data:
                print(data)
        else:
            print(risk_data)

    def test_get_inst_sim_pnl(self):
        risk_data = risk.get_inst_sim_pnl(['2171035.IB', '2105288.IB'], '2024-05-28', '2024-05-27')
        if risk_data is not None:
            for data in risk_data:
                print(data)
        else:
            print(risk_data)

    def test_get_inst_stressed_pnl(self):
        risk_data = risk.get_inst_stressed_pnl(['2171035.IB', '2105288.IB'], '2024-05-28', '2024-05-27')
        if risk_data is not None:
            for data in risk_data:
                print(data)
        else:
            print(risk_data)

    def test_get_inst_var(self):
        risk_data = risk.get_inst_var("2171035.IB", '2024-05-28', '2024-05-27', ['var', 'es'])
        if risk_data is not None:
            print(risk_data)
        else:
            print(risk_data)
