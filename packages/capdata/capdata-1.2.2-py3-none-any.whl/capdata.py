import request.request as rq

import data.curve
import data.market
import data.pricing
import data.refer
import data.risk
from typing import List

"""
capdata 认证
"""


def init(name, pwd):
    auth_json = {'account': name, 'pwd': pwd}
    token = rq.post_no_token("/capdata/auth", auth_json)
    rq.save_token(token)
    print('登录成功')


"""
   获取债券收益率曲线
   参数:
     curve -- 曲线编码
     start -- 开始时间
     end -- 结束时间
     freq -- 频率(1m, d, w)
     parse_proto -- 是否转化曲线,默认True
     window -- 时间窗口 ['10:00:00','10:30:00']
   """


def get_bond_yield_curve(curve, start, end, freq='d', parse_proto=True, window=None):
    return data.curve.get_bond_yield_curve(curve, start, end, freq, window, parse_proto)


"""
获取信用利差曲线
参数:
  curve -- 曲线编码
  start -- 开始时间
  end -- 结束时间
  freq -- 频率(1m, d, w)
  parse_proto -- 是否转化曲线,默认True
  window -- 时间窗口 ['10:00:00','10:30:00']
"""


def get_bond_spread_curve(curve, start, end, freq='d', parse_proto=True, window=None):
    return data.curve.get_bond_spread_curve(curve, start, end, freq, window, parse_proto)


"""
获取利率收益率曲线
参数:
  curve -- 曲线编码
  start -- 开始时间
  end -- 结束时间
  freq -- 频率(1m, d, w)
  parse_proto -- 是否转化曲线,默认True
  window -- 时间窗口 ['10:00:00','10:30:00']
"""


def get_ir_yield_curve(curve, start, end, freq='d', parse_proto=True, window=None):
    return data.curve.get_ir_yield_curve(curve, start, end, freq, window, parse_proto)


"""
获取股息分红率曲线
参数:
  curve -- 曲线编码
  start -- 开始时间
  end -- 结束时间
  freq -- 频率(1m, d, w)
  parse_proto -- 是否转化曲线,默认True
  window -- 时间窗口 ['10:00:00','10:30:00']
"""


def get_dividend_curve(curve, start, end, freq='d', parse_proto=True, window=None):
    return data.curve.get_dividend_curve(curve, start, end, freq, window, parse_proto)


"""
获取波动率曲面数据
参数:
  surface -- 波动率曲面编码
  start -- 开始时间
  end -- 结束时间
  freq -- 频率(1m, d, w)
  window -- 时间窗口 ['10:00:00','10:30:00']
"""


def get_vol_surface(surface, start, end, freq='d', window=None):
    return data.curve.get_vol_surface(surface, start, end, freq, window)


"""
   获取历史行情数据
   参数:
       inst -- 产品编码列表 ['200310.IB', '190008.IB']
       start -- 开始时间  2024-05-09
       end -- 结束时间  2024-05-10
       fields -- 需要返回的字段(open、close、high、low、open_ytm、close_ytm、high_ytm、low_ytm、adv_5d、adv_10d、adv_20d、
       pre_adj_close、post_adj_close、volume、turnover、num_trades、settlement、vwap、
       open_interest、bid、ask、bid_size、ask_size、trade、trade_size、level1、level2、level2_5、level2_10、lix)  ['bid','ask']
       freq  -- 频率( 1m,1h, d, w)
       window -- 时间窗口 ['10:00:00','10:30:00']
       mkt -- 市场
       clazz -- 产品类别
   """


def get_hist_mkt(inst, start, end, fields, window=None, mkt=None, freq="d", clazz: str = None):
    return data.market.get_hist_mkt(inst, start, end, fields, window, mkt, freq, clazz)


"""
获取日内实时行情数据
参数:
  inst -- 产品编码列表 ['200310.IB', '190008.IB']
  fields -- 需要返回的字段(bid、ask、level1、level2、level2_5、level2_10、lix)  ['bid','ask']
  mkt -- 市场   
"""


def get_live_mkt(inst, fields, mkt=""):
    return data.market.get_live_mkt(inst, fields, mkt)


"""
获取产品定价数据
参数:
    inst -- 产品编码列表 ['2292030.IB', '2292012.IB']
    start -- 开始时间  2024-05-26
    end -- 结束时间  2024-05-29
    fields -- 需要返回的字段(price、duration、modified_duration、macaulay_duration、convexity、z_spread、dv01、bucket_dv01、cs01、
    bucket_cs01、delta、gamma、vega、term_bucket_vega、term_strike_bucket_vega、volga、term_bucket_volga、term_strike_bucket_volga、
    vanna、term_bucket_vanna、term_strike_bucket_vanna、rho)  ['duration','modified_duration']
    freq  -- 频率( 1m, d, w)
    window -- 时间窗口 ['10:00:00','10:30:00']
"""


def get_pricing(inst, start, end, fields, window=None, mkt=None, freq="d"):
    return data.pricing.get_pricing(inst, start, end, fields, window, mkt, freq)


"""
获取产品估值数据
参数:
    inst -- 产品编码列表 ['2292030.IB', '2292012.IB']
    start -- 开始时间  2024-05-26
    end -- 结束时间  2024-05-29
    fields -- 需要返回的字段(present_value、dv01、bucket_dv01、frtb_bucket_dv01、cs01、bucket_cs01、frtb_bucket_cs01、delta、frtb_delta、
     gamma、frtb_curvature、vega、term_bucket_vega、term_strike_bucket_vega、frtb_vega、volga、term_bucket_volga、term_strike_bucket_volga、
     vanna、term_bucket_vanna、term_strike_bucket_vanna、rho)  ['dv01','cs01']
    freq  -- 频率( 1m, d, w)
    window -- 时间窗口 ['10:00:00','10:30:00']
"""


def get_valuation(inst, start, end, fields, window=None, mkt=None, freq="d"):
    return data.pricing.get_valuation(inst, start, end, fields, window, mkt, freq)


"""
获取债券收益率曲线情景模拟数据
参数:
  curve -- 曲线编码  CN_TREAS_STD_SIM
  sim_date -- 情景时间  2024-01-05
  base_date -- 基础时间 2024-01-04
  num_start -- 情景开始数   0
  num_end -- 情景结束数   500
  parse_proto -- 是否转化proto  False
"""


def get_sim_bond_yield_curve(curve, sim_date, base_date, num_start=0, num_end=500, parse_proto=False):
    return data.risk.get_sim_bond_yield_curve(curve, sim_date, base_date, num_start, num_end, parse_proto)

    """
    获取历史模拟的利率收益率曲线数据
    参数:
      curve -- 曲线编码  CN_TREAS_STD
      sim_date -- 情景时间  2024-05-28
      num_sims -- 情景数   200
      base_date -- 基础时间 2024-05-27
    """


def get_hist_sim_ir_curve(curve, sim_date, base_date, num_sims=200):
    return data.risk.get_hist_sim_ir_curve(curve, sim_date, base_date, num_sims)


"""
获取历史模拟的信用利差曲线数据
参数:
  curve -- 曲线编码  CN_CORP_AAA_SPRD_STD
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_hist_sim_credit_curve(curve, sim_date, base_date, num_sims=200):
    return data.risk.get_hist_sim_credit_curve(curve, sim_date, base_date, num_sims)


"""
获取历史压力情景下利率收益率曲线数据
参数:
  curve -- 曲线编码  CN_TREAS_STD
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_hist_stressed_ir_curve(curve, sim_date, base_date, num_sims=200):
    return data.risk.get_hist_stressed_ir_curve(curve, sim_date, base_date, num_sims)


"""
获取历史压力情景下信用利差曲线数据
参数:
  curve -- 曲线编码  CN_CORP_AAA_SPRD_STD
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_hist_stressed_credit_curve(curve, sim_date, base_date, num_sims=200):
    return data.risk.get_hist_sim_credit_curve(curve, sim_date, base_date, num_sims)


"""
获取产品模拟情景下损益数据
参数:
  inst -- 产品编码  ['2171035.IB','2105288.IB']
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_inst_sim_pnl(inst, sim_date, base_date, num_sims=200):
    return data.risk.get_inst_sim_pnl(inst, sim_date, base_date, num_sims)


"""
获取产品压力情景下损益数据
参数:
  inst -- 产品编码  ['2171035.IB','2105288.IB']
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_inst_stressed_pnl(inst, sim_date, base_date, num_sims=200):
    return data.risk.get_inst_stressed_pnl(inst, sim_date, base_date, num_sims)


"""
获取产品Value-at-Risk数据
参数:
  inst -- 产品编码  2171035.IB
  sim_date -- 情景时间  2024-05-28 
  base_date -- 基础时间 2024-05-27
  fields -- 响应字段 (var, mirror_var, stressed_var, mirror_stressed_var, es, mirror_es, stressed_es, mirror_stressed_es) ['var','es']
  confidence_interval  -- 置信区间 0.95
"""


def get_inst_var(inst, sim_date, base_date, fields, confidence_interval=0.95):
    return data.risk.get_inst_var(inst, sim_date, base_date, fields, confidence_interval)


# 参考数据
"""
获取指定日历下的假期数据
参数:
  calendar -- 日历 CFETS
"""


def get_holidays(calendar: str):
    return data.refer.get_holidays(calendar)


"""
获取基准利率列表
参数:
  ccy -- 基准利率编码列表 ['CNY']
"""


def get_ir_index(ccy: List[str]):
    return data.refer.get_ir_index(ccy)


"""
获取基准利率定义数据
参数:
  ir_index -- 产品编码列表 ['FR_001','FR_007']
"""


def get_ir_index_definition(ir_index: List[str]):
    return data.refer.get_ir_index_definition(ir_index)


"""
获取利率收益率曲线列表
参数:
  ccy -- 货币列表 ['CNY']
  ir_index -- 基准利率列表 ['FR_007']
"""


def get_ir_curve_list(ccy: List[str], ir_index: List[str]):
    return data.refer.get_ir_curve_list(ccy, ir_index)


"""
获取利率收益率曲线定义
参数:
  curve_codes -- 曲线编码列表 ['CNY_FR_007'] 
"""


def get_ir_curve_definition(curve_codes: List[str]):
    return data.refer.get_ir_curve_definition(curve_codes)


"""
获取债券收益率曲线列表
参数:
  ccy -- 货币列表 ['CNY']
  ir_index -- 基准利率列表 []
"""


def get_bond_yield_curve_list(ccy: List[str], ir_index: List[str]):
    return data.refer.get_bond_yield_curve_list(ccy, ir_index, 'MKT')


"""
获取标准债券收益率曲线列表
参数:
  ccy -- 货币列表 ['CNY']
  ir_index -- 基准利率列表 []
"""


def get_std_bond_yield_curve_list(ccy: List[str], ir_index: List[str]):
    return data.refer.get_bond_yield_curve_list(ccy, ir_index, 'STD')


"""
获取债券收益率曲线定义
参数:
  curve_codes -- 曲线编码列表 ['CN_RAILWAY_MKT'，'CN_CLO_LEASE_ABS_AA_STD'] 
"""


def get_bond_yield_curve_definition(curve_codes: List[str]):
    return data.refer.get_bond_yield_curve_definition(curve_codes)


"""
获取债券信用利差曲线列表
参数:
  ccy -- 货币列表 ['CNY']
  ir_index -- 基准利率列表 []
"""


def get_bond_credit_curve_list(ccy: List[str], ir_index: List[str]):
    return data.refer.get_bond_credit_curve_list(ccy, ir_index, 'MKT')


"""
获取标准债券信用利差曲线列表
参数:
  ccy -- 货币列表 ['CNY']
  ir_index -- 基准利率列表 []
"""


def get_std_bond_credit_curve_list(ccy: List[str], ir_index: List[str]):
    return data.refer.get_bond_credit_curve_list(ccy, ir_index, 'STD')


"""
获取债券信用利差曲线定义
参数:
  curve_codes -- 曲线编码列表 ['CN_SP_MTN_AA+_SPRD_STD'，'CN_CORP_AAA-_SPRD_STD'] 
"""


def get_bond_credit_curve_definition(curve_codes: List[str]):
    return data.refer.get_bond_credit_curve_definition(curve_codes)


"""
获取债券列表
参数:
  market -- 市场列表  ['CN_INTER_BANK']
  ccy -- 货币列表 ['CNY']
  bond_mkt_type -- 市场类型列表 ['国债']
  bond_inst_type -- 产品类型列表 ['FIXED_COUPON_BOND']
  credit_rating  -- 信用等级列表 []
"""


def get_bond_list(market: List[str], ccy: List[str], bond_mkt_type: List[str], bond_inst_type: List[str],
                  credit_rating: List[str]):
    return data.refer.get_bond_list(market, ccy, bond_mkt_type, bond_inst_type, credit_rating, False)


"""
获取标准债券列表
参数: 
  ccy -- 货币列表 ['CNY']
  bond_mkt_type -- 市场类型列表 ['国债']
  bond_inst_type -- 产品类型列表 ['FIXED_COUPON_BOND']
  credit_rating  -- 信用等级列表 []
"""


def get_std_bond_list(ccy: List[str], bond_mkt_type: List[str], bond_inst_type: List[str],
                      credit_rating: List[str]):
    return data.refer.get_bond_list([], ccy, bond_mkt_type, bond_inst_type, credit_rating, True)


"""
获取债券定义
参数:
  bond_code -- 债券编码列表 ['050220.IB','060203.IB'] 
"""


def get_bond_definition(bond_code: List[str]):
    return data.refer.get_bond_definition(bond_code)


"""
获取债券定价setting
参数:
  bond_code -- 债券编码列表 ['050220.IB','060203.IB'] 
"""


def get_bond_pricing_settings(bond_code: List[str]):
    return data.refer.get_bond_pricing_settings(bond_code)


"""
获取债券估值setting
参数:
  bond_code -- 债券编码列表 ['050220.IB'，'060203.IB'] 
"""


def get_bond_valuation_settings(bond_code: List[str]):
    return data.refer.get_bond_valuation_settings(bond_code)


"""
获取债券情景估值setting
参数:
  bond_code -- 债券编码列表 ['050220.IB','060203.IB'] 
"""


def get_bond_sim_valuation_settings(bond_code: List[str]):
    return data.refer.get_bond_sim_valuation_settings(bond_code)


"""
获取风险因子定义
参数:
  risk_factor_code -- 风险因子编码列表 ['RF_CN_TREAS_ZERO_1M'] 
"""


def get_risk_factor_definition(risk_factor_code: List[str]):
    return data.refer.get_risk_factor_definition(risk_factor_code)


"""
获取风险因子组定义
参数:
  risk_factor_group -- 风险因子组编码列表 ['FI_BOND_IR_CN_IB_HIST_SIM_SCN_GROUP'] 
"""


def get_risk_factor_group_definition(risk_factor_group: List[str]):
    return data.refer.get_risk_factor_group_definition(risk_factor_group)


"""
获取利率产品定义
参数： 
  inst_type  -- 产品类型列表,必填，可选 SWAP, CROSS, DEPO  ['DEPO']
  inst_codes -- 产品编码  []
  ccy       -- 货币 ['CNY']
  ir_index   -- 基准利率列表 []
"""


def get_ir_vanilla_instrument_definition(inst_codes: []):
    if (inst_codes is None or len(inst_codes) == 0):
        raise ValueError(f'inst_codes 值不能空')
    return data.refer.get_ir_vanilla_instrument_definition(inst_codes)


"""
获取利率互换列表
参数：
   swap_type  -- 互换类型列表,预留字段 []
   ccy       -- 货币 ['CNY']
   ir_index   -- 基准利率列表 []
"""


def get_ir_vanilla_swap_list(ccy: [] = None, ir_index: [] = None, swap_type: [] = None):
    return data.refer.get_ir_vanilla_swap_list(ccy, ir_index, swap_type)


"""
获取同业拆借列表
参数： 
   ccy  -- 货币 ['CNY']
"""


def get_ir_depo_list(ccy: [] = None):
    return data.refer.get_ir_depo_list(ccy)


"""
获取交叉货币列表
参数： 
   ccy       -- 货币 ['CNY']
   ir_index   -- 基准利率列表 []
"""


def get_xccy_swap_list(ccy: [] = None, ir_index: [] = None):
    return data.refer.get_xccy_swap_list(ccy, ir_index)
