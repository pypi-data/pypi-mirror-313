import request.request as rq

"""
获取债券收益率曲线
参数:
  curve -- 曲线编码
  start -- 开始时间
  end -- 结束时间
  freq -- 频率(1m, d, w)
  window -- 时间窗口 ['10:00:00','10:30:00']
  parse_proto -- 是否转化曲线,默认True
"""


def get_bond_yield_curve(curve, start, end, freq='d', window=None, parse_proto=True):
    data_json = {'curve': curve, 'start': start, 'end': end, 'freq': freq, 'window': window, 'parseProto': parse_proto}
    return rq.post_token("/capdata/get/bond/curve", data_json)


"""
获取信用利差曲线
参数:
  curve -- 曲线编码
  start -- 开始时间
  end -- 结束时间
  freq -- 频率(1m, d, w)
  window -- 时间窗口 ['10:00:00','10:30:00']
  parse_proto -- 是否转化曲线,默认True
"""


def get_bond_spread_curve(curve, start, end, freq='d', window=None, parse_proto=True):
    data_json = {'curve': curve, 'start': start, 'end': end, 'freq': freq, 'window': window, 'parseProto': parse_proto}
    return rq.post_token("/capdata/get/credit/curve", data_json)


"""
获取利率收益率曲线
参数:
  curve -- 曲线编码
  start -- 开始时间
  end -- 结束时间
  freq -- 频率(1m, d, w)
  window -- 时间窗口 ['10:00:00','10:30:00']
  parse_proto -- 是否转化曲线,默认True
"""


def get_ir_yield_curve(curve, start, end, freq='d', window=None, parse_proto=True):
    data_json = {'curve': curve, 'start': start, 'end': end, 'freq': freq, 'window': window, 'parseProto': parse_proto}
    return rq.post_token("/capdata/get/ir/curve", data_json)


"""
获取股息分红率曲线
参数:
  curve -- 曲线编码
  start -- 开始时间
  end -- 结束时间
  freq -- 频率(1m, d, w)
  window -- 时间窗口 ['10:00:00','10:30:00']
  parse_proto -- 是否转化曲线,默认True
"""


def get_dividend_curve(curve, start, end, freq='d', window=None, parse_proto=True):
    data_json = {'curve': curve, 'start': start, 'end': end, 'freq': freq, 'window': window, 'parseProto': parse_proto}
    return rq.post_token("/capdata/get/dividend/curve", data_json)


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
    data_json = {'surface': surface, 'start': start, 'end': end, 'freq': freq, 'window': window}
    return rq.post_token("/capdata/get/fx/vol/surface", data_json)
