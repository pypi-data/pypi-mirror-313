import json
import sqlite3
from typing import Any
import requests

from request import PATH


# post token请求
def post_token(url, params: Any):
    headers = {'Accept': 'application/json', 'content-type': 'application/json', 'Accept-Encoding': 'gzip',
               'x-access-token': _get_token()}
    return _post(url, params, headers)


# post 无token请求
def post_no_token(url, params):
    headers = {'Accept': 'application/json', 'content-type': 'application/json'}
    return _post(url, params, headers)


# post 请求
def _post(url, params, headers):
    response = requests.post(PATH + url, json=params, headers=headers).text
    res = json.loads(response)
    code = res["respCode"]
    if str(code) == 'SUCCEED':
        if 'data' in res:
            return res["data"]
        else:
            return None
    else:
        raise Exception(res["message"])


# 存储token
def save_token(token):
    # 连接到数据库，如果不存在则会自动创建
    conn = sqlite3.connect('token.db')
    # 创建游标对象
    cursor = conn.cursor()
    cursor.execute("drop TABLE IF EXISTS t_token ")
    # 创建表
    cursor.execute('''CREATE TABLE IF NOT EXISTS t_token
                       (token text)''')
    # 插入数据
    cursor.execute("INSERT INTO t_token VALUES (?)", (token,))
    # 提交事务
    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()


def _get_token():
    try:
        # 连接到数据库，如果不存在则会自动创建
        conn = sqlite3.connect('token.db')
        # 创建游标对象
        cursor = conn.cursor()
        # 查询数据
        cursor.execute("select * from t_token")
        token = cursor.fetchone()
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()
        return token[0]
    except Exception:
        raise Exception("未登录，请先登录")
