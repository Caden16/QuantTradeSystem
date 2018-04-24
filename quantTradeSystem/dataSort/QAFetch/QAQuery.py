# coding: utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import datetime

import numpy
import pandas as pd
from pandas import DataFrame

from ..QAUtil import (DATABASE, QA_Setting, QA_util_date_stamp,
                              QA_util_date_valid, QA_util_dict_remove_key,
                              QA_util_log_info,
                              QA_util_sql_mongo_sort_DESCENDING,
                              QA_util_time_stamp, QA_util_to_json_from_pandas,
                              trade_date_sse)


"""
按要求从数据库取数据，并转换成numpy结构

"""


def QA_fetch_stock_day(code, start, end, format='numpy', frequence='day', collections=DATABASE.stock_day):
    '获取股票日线'
    start = str(start)[0:10]
    end = str(end)[0:10]

    if QA_util_date_valid(end) == True:

        __data = []
        cursor = collections.find({
            'code': str(code)[0:6], "date_stamp": {
                "$lte": QA_util_date_stamp(end),
                "$gte": QA_util_date_stamp(start)}})
        if format in ['json', 'dict']:
            return [QA_util_dict_remove_key(data, '_id') for data in cursor]

        for item in cursor:
            __data.append([str(item['code']), float(item['open']), float(item['high']), float(
                item['low']), float(item['close']), float(item['vol']), item['date']])

        # 多种数据格式
        if format in ['n', 'N', 'numpy']:
            __data = numpy.asarray(__data)
        elif format in ['list', 'l', 'L']:
            __data = __data
        elif format in ['P', 'p', 'pandas', 'pd']:

            __data = DataFrame(__data, columns=[
                'code', 'open', 'high', 'low', 'close', 'volume', 'date'])

            __data['date'] = pd.to_datetime(__data['date'])
            __data = __data.set_index('date', drop=False)

        return __data
    else:
        QA_util_log_info('something wrong with date')


def QA_fetch_stock_min(code, start, end, format='numpy', frequence='1min', collections=DATABASE.stock_min):
    '获取股票分钟线'
    if frequence in ['1min', '1m']:
        frequence = '1min'
    elif frequence in ['5min', '5m']:
        frequence = '5min'
    elif frequence in ['15min', '15m']:
        frequence = '15min'
    elif frequence in ['30min', '30m']:
        frequence = '30min'
    elif frequence in ['60min', '60m']:
        frequence = '60min'
    __data = []
    cursor = collections.find({
        'code': str(code), "time_stamp": {
            "$gte": QA_util_time_stamp(start),
            "$lte": QA_util_time_stamp(end)
        }, 'type': frequence
    })
    if format in ['dict', 'json']:
        return [data for data in cursor]
    for item in cursor:

        __data.append([str(item['code']), float(item['open']), float(item['high']), float(
            item['low']), float(item['close']), float(item['vol']), item['datetime'], item['time_stamp'], item['date']])

    __data = DataFrame(__data, columns=[
        'code', 'open', 'high', 'low', 'close', 'volume', 'datetime', 'time_stamp', 'date'])

    __data['datetime'] = pd.to_datetime(__data['datetime'])
    __data = __data.set_index('datetime', drop=False)
    if format in ['numpy', 'np', 'n']:
        return numpy.asarray(__data)
    elif format in ['list', 'l', 'L']:
        return numpy.asarray(__data).tolist()
    elif format in ['P', 'p', 'pandas', 'pd']:
        return __data


def QA_fetch_stocklist_min(stock_list, date_range, frequence='1min', collections=DATABASE.stock_min):
    '获取不复权股票分钟线'
    __data = []
    for item in stock_list:
        __data.append(QA_fetch_stock_min(
            item, date_range[0], date_range[-1], 'pd', frequence, collections))
    return __data


def QA_fetch_trade_date():
    '获取交易日期'
    return trade_date_sse


def QA_fetch_stock_list(collections=DATABASE.stock_list):
    '获取股票列表'
    return [item for item in collections.find()]


def QA_fetch_stock_full(date, format='numpy', collections=DATABASE.stock_day):
    '获取全市场的某一日的数据'
    Date = str(date)[0:10]
    if QA_util_date_valid(Date) is True:

        __data = []
        for item in collections.find({
            "date_stamp": {
                "$lte": QA_util_date_stamp(Date),
                "$gte": QA_util_date_stamp(Date)}}):
            __data.append([str(item['code']), float(item['open']), float(item['high']), float(
                item['low']), float(item['close']), float(item['vol']), item['date']])
        # 多种数据格式
        if format in ['n', 'N', 'numpy']:
            __data = numpy.asarray(__data)
        elif format in ['list', 'l', 'L']:
            __data = __data
        elif format in ['P', 'p', 'pandas', 'pd']:
            __data = DataFrame(__data, columns=[
                'code', 'open', 'high', 'low', 'close', 'volume', 'date'])
            __data['date'] = pd.to_datetime(__data['date'])
            __data = __data.set_index('date', drop=False)
        return __data
    else:
        QA_util_log_info('something wrong with date')


def QA_fetch_stocklist_day(stock_list, date_range, collections=DATABASE.stock_day):
    '获取多个股票的日线'
    __data = []
    for item in stock_list:
        __data.append(QA_fetch_stock_day(
            item, date_range[0], date_range[-1], 'pd', collections))
    return __data


def QA_fetch_index_day(code, start, end, format='numpy', collections=DATABASE.index_day):
    '获取指数日线'
    start = str(start)[0:10]
    end = str(end)[0:10]

    if QA_util_date_valid(end) == True:

        __data = []
        cursor = collections.find({
            'code': str(code)[0:6], "date_stamp": {
                "$lte": QA_util_date_stamp(end),
                "$gte": QA_util_date_stamp(start)}})
        if format in ['dict', 'json']:
            return [data for data in cursor]
        for item in cursor:

            __data.append([str(item['code']), float(item['open']), float(item['high']), float(
                item['low']), float(item['close']), float(item['vol']), item['date']])

        # 多种数据格式
        if format in ['n', 'N', 'numpy']:
            __data = numpy.asarray(__data)
        elif format in ['list', 'l', 'L']:
            __data = __data
        elif format in ['P', 'p', 'pandas', 'pd']:

            __data = DataFrame(__data, columns=[
                'code', 'open', 'high', 'low', 'close', 'volume', 'date'])

            __data['date'] = pd.to_datetime(__data['date'])
            __data = __data.set_index('date', drop=False)
        return __data
    else:
        QA_util_log_info('something wrong with date')


def QA_fetch_indexlist_day(stock_list, date_range, collections=DATABASE.index_day):
    '获取多个股票的日线'
    __data = []
    for item in stock_list:
        __data.append(QA_fetch_index_day(
            item, date_range[0], date_range[-1], 'pd', collections))
    return __data


def QA_fetch_index_min(
        code,
        start, end,
        format='numpy',
        frequence='1min',
        collections=DATABASE.index_min):
    '获取股票分钟线'
    if frequence in ['1min', '1m']:
        frequence = '1min'
    elif frequence in ['5min', '5m']:
        frequence = '5min'
    elif frequence in ['15min', '15m']:
        frequence = '15min'
    elif frequence in ['30min', '30m']:
        frequence = '30min'
    elif frequence in ['60min', '60m']:
        frequence = '60min'
    __data = []

    cursor = collections.find({
        'code': str(code), "time_stamp": {
            "$gte": QA_util_time_stamp(start),
            "$lte": QA_util_time_stamp(end)
        }, 'type': frequence
    })
    if format in ['dict', 'json']:
        return [data for data in cursor]
    for item in cursor:

        __data.append([str(item['code']), float(item['open']), float(item['high']), float(
            item['low']), float(item['close']), float(item['vol']), item['datetime'], item['time_stamp'], item['date']])

    __data = DataFrame(__data, columns=[
        'code', 'open', 'high', 'low', 'close', 'volume', 'datetime', 'time_stamp', 'date'])

    __data['datetime'] = pd.to_datetime(__data['datetime'])
    __data = __data.set_index('datetime', drop=False)
    if format in ['numpy', 'np', 'n']:
        return numpy.asarray(__data)
    elif format in ['list', 'l', 'L']:
        return numpy.asarray(__data).tolist()
    elif format in ['P', 'p', 'pandas', 'pd']:
        return __data


def QA_fetch_future_day():
    pass


def QA_fetch_future_min():
    pass


def QA_fetch_future_tick():
    pass


def QA_fetch_stock_xdxr(code, format='pd', collections=DATABASE.stock_xdxr):
    '获取股票除权信息/数据库'
    data = pd.DataFrame([item for item in collections.find(
        {'code': code})]).drop(['_id'], axis=1)
    data['date'] = pd.to_datetime(data['date'])
    return data.set_index('date', drop=False)


def QA_fetch_backtest_info(user=None, account_cookie=None, strategy=None, stock_list=None, collections=DATABASE.backtest_info):

    return QA_util_to_json_from_pandas(pd.DataFrame([item for item in collections.find(QA_util_to_json_from_pandas(pd.DataFrame([user, account_cookie, strategy, stock_list], index=['user', 'account_cookie', 'strategy', 'stock_list']).dropna().T)[0])]).drop(['_id'], axis=1))


def QA_fetch_backtest_history(cookie=None, collections=DATABASE.backtest_history):
    return QA_util_to_json_from_pandas(pd.DataFrame([item for item in collections.find(QA_util_to_json_from_pandas(pd.DataFrame([cookie], index=['cookie']).dropna().T)[0])]).drop(['_id'], axis=1))


def QA_fetch_stock_block(code=None, format='pd', collections=DATABASE.stock_block):
    if code is not None:
        data = pd.DataFrame([item for item in collections.find(
            {'code': code})]).drop(['_id'], axis=1)
        return data.set_index('code', drop=False)
    else:
        data = pd.DataFrame(
            [item for item in collections.find()]).drop(['_id'], axis=1)
        return data.set_index('code', drop=False)


def QA_fetch_stock_info(code, format='pd', collections=DATABASE.stock_info):
    try:
        data = pd.DataFrame([item for item in collections.find(
            {'code': code})]).drop(['_id'], axis=1)
        #data['date'] = pd.to_datetime(data['date'])
        return data.set_index('code', drop=False)
    except Exception as e:
        QA_util_log_info(e)
        return None


def QA_fetch_stock_name(code, collections=DATABASE.stock_list):
    try:
        return collections.find_one({'code': code})['name']
    except Exception as e:
        QA_util_log_info(e)


def QA_fetch_quotation(code, date=datetime.date.today(), db=DATABASE):
    '获取某一只实时5档行情的存储结果'
    try:
        collections = db.get_collection(
            'realtime_{}'.format(date))
        return pd.DataFrame([item for item in collections.find(
            {'code': code})]).drop(['_id'], axis=1).set_index('datetime', drop=False).sort_index()
    except Exception as e:
        raise e


def QA_fetch_quotations(date=datetime.date.today(), db=DATABASE):
    '获取全部实时5档行情的存储结果'
    try:
        collections = db.get_collection(
            'realtime_{}'.format(date))
        return pd.DataFrame([item for item in collections.find(
            {})]).drop(['_id'], axis=1).set_index('datetime', drop=False).sort_index()
    except Exception as e:
        raise e


def QA_fetch_account(message={}, db=DATABASE):
    """get the account

    Arguments:
        query_mes {[type]} -- [description]

    Keyword Arguments:
        collection {[type]} -- [description] (default: {DATABASE})

    Returns:
        [type] -- [description]
    """
    collection = DATABASE.account
    return [QA_util_dict_remove_key(res, '_id') for res in collection.find(message)]


if __name__ == '__main__':
    print(QA_fetch_quotations('000001'))
