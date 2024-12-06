import request.request as rq

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
    data_json = {'inst': inst, 'start': start, 'end': end, 'freq': freq, 'window': window, 'mkt': mkt,
                 'fields': fields}
    return rq.post_token("/capdata/get/pricing", data_json)


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
    data_json = {'inst': inst, 'start': start, 'end': end, 'freq': freq, 'window': window, 'mkt': mkt,
                 'fields': fields}
    return rq.post_token("/capdata/get/valuation", data_json)
