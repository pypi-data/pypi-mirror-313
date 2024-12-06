import request.request as rq
import pandas

inst_type = ["BOND", "BOND_FUTURE", "CDS", "COMMODITY_FUTURE", "COMMODITY_OPTION", "COMMODITY_SPOT", "COMMODITY_SWAP",
             "FX", "IBOR", "IR", "STOCK_FUTURE", "STOCK_OPTION", "STOCK_SPOT"]

"""
获取历史行情数据
参数:
    inst -- 产品编码列表 ['200310.IB', '190008.IB']

    start -- 开始时间  2024-05-09

    end -- 结束时间  2024-05-10

    fields -- 需要返回的字段(open、close、high、low、pre_adj_close、post_adj_close、volume、turnover、num_trades、settlement、
    open_interest、bid、ask、bid_size、ask_size、trade、trade_size、level1、level2、level2_5、level2_10、lix)  ['bid','ask']

    freq  -- 频率( 1m,1h, d, w)

    window -- 时间窗口 ['10:00:00','10:30:00']

    mkt -- 市场
    clazz -- 产品类别
"""


def get_hist_mkt(inst, start, end, fields, window=None, mkt=None, freq="d", clazz: str = None):
    if clazz is not None and clazz not in inst_type:
        raise ValueError(f'clazz 值不正确，可选值为{inst_type}')
    data_json = {'inst': inst, 'start': start, 'end': end, 'freq': freq, 'window': window, 'mkt': mkt,
                 'fields': fields, 'instType': clazz}
    result = rq.post_token("/capdata/get/hist/mkt", data_json)
    df = pandas.DataFrame(result)
    if len(df) > 0:
        df['date'] = pandas.to_datetime(df['date'])
        df = df.sort_values(by='date')
        if freq == 'd' or freq == 'w':
            col = ['inst', 'date'] + fields
            df = df.reindex(columns=col)
        else:
            col = ['inst', 'date', 'time'] + fields
            df = df.reindex(columns=col)
            df['time'] = df['date'].dt.time
        df['date'] = df['date'].dt.date
        return df
    else:
        return df


"""
获取日内实时行情数据
参数:
  inst -- 产品编码列表 ['200310.IB', '190008.IB']

  fields -- 需要返回的字段(bid、ask、level1、level2、level2_5、level2_10、lix)  ['bid','ask']

  mkt -- 市场   
"""


def get_live_mkt(inst, fields, mkt=""):
    data_json = {'inst': inst, 'mkt': mkt, 'fields': fields}
    result = rq.post_token("/capdata/get/live/mkt", data_json)
    df = pandas.DataFrame(result)
    if len(df) > 0:
        df['date'] = pandas.to_datetime(df['date'])
        df = df.sort_values(by='date')
        col = ['inst', 'date', 'time'] + fields
        df = df.reindex(columns=col)
        df['time'] = df['date'].dt.time
        df['date'] = df['date'].dt.date
        return df
    else:
        return df
