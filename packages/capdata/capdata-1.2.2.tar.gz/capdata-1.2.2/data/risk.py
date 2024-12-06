import request.request as rq

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
    data_json = {'curve': curve, 'simDate': sim_date, 'baseDate': base_date, 'numStart': num_start, 'numEnd': num_end,
                 'parseProto': parse_proto}
    return rq.post_token("/capdata/get/sim/bond/yield/curve", data_json)


"""
获取历史模拟的利率收益率曲线数据
参数:
  curve -- 曲线编码  CN_TREAS_STD
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_hist_sim_ir_curve(curve, sim_date, base_date, num_sims=200):
    data_json = {'curve': curve, 'simDate': sim_date, 'baseDate': base_date, 'numSims': num_sims}
    return rq.post_token("/capdata/get/sim/ir/curve", data_json)


"""
获取历史模拟的信用利差曲线数据
参数:
  curve -- 曲线编码  CN_CORP_AAA_SPRD_STD
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_hist_sim_credit_curve(curve, sim_date, base_date, num_sims=200):
    data_json = {'curve': curve, 'simDate': sim_date, 'baseDate': base_date, 'numSims': num_sims}
    return rq.post_token("/capdata/get/sim/bond/spread/curve", data_json)


"""
获取历史压力情景下利率收益率曲线数据
参数:
  curve -- 曲线编码  CN_TREAS_STD
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_hist_stressed_ir_curve(curve, sim_date, base_date, num_sims=200):
    data_json = {'curve': curve, 'simDate': sim_date, 'baseDate': base_date, 'numSims': num_sims}
    return rq.post_token("/capdata/get/sim/stressed/ir/curve", data_json)


"""
获取历史压力情景下信用利差曲线数据
参数:
  curve -- 曲线编码  CN_CORP_AAA_SPRD_STD
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_hist_stressed_credit_curve(curve, sim_date, base_date, num_sims=200):
    data_json = {'curve': curve, 'simDate': sim_date, 'baseDate': base_date, 'numSims': num_sims}
    return rq.post_token("/capdata/get/hist/stressed/credit/curve", data_json)


"""
获取产品模拟情景下损益数据
参数:
  inst -- 产品编码  ['2171035.IB','2105288.IB']
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_inst_sim_pnl(inst, sim_date, base_date, num_sims=200):
    data_json = {'inst': inst, 'simDate': sim_date, 'baseDate': base_date, 'numSims': num_sims}
    return rq.post_token("/capdata/get/inst/sim/pnl", data_json)


"""
获取产品压力情景下损益数据
参数:
  inst -- 产品编码  ['2171035.IB','2105288.IB']
  sim_date -- 情景时间  2024-05-28
  num_sims -- 情景数   200
  base_date -- 基础时间 2024-05-27
"""


def get_inst_stressed_pnl(inst, sim_date, base_date, num_sims=200):
    data_json = {'inst': inst, 'simDate': sim_date, 'baseDate': base_date, 'numSims': num_sims}
    return rq.post_token("/capdata/get/inst/stressed/pnl", data_json)


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
    data_json = {'inst': inst, 'simDate': sim_date, 'baseDate': base_date, 'fields': fields,
                 'confidenceInterval': confidence_interval}
    return rq.post_token("/capdata/get/inst/risk/metrics", data_json)
