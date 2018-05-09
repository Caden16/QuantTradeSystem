# coding:utf-8
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
import threading
import time

from ..QAUtil.QALogs import QA_util_log_info


def QA_util_time_now():
    """[summary]
    
    Returns:
        [type] -- [description]
    """

    return datetime.datetime.now()


def QA_util_date_today():
    """[summary]
    
    Returns:
        [type] -- [description]
    """

    return datetime.date.today()


def QA_util_date_str2int(date):
    """[summary]
    
    Arguments:
        date {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    return int(str(date)[0:4] + str(date)[5:7] + str(date)[8:10])


def QA_util_date_int2str(date):
    """[summary]
    
    Arguments:
        date {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    return str(str(date)[0:4] + '-' + str(date)[4:6] + '-' + str(date)[6:8])


def QA_util_to_datetime(time):
    """[summary]
    
    Arguments:
        time {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    if len(str(time)) == 10:
        _time = '{} 00:00:00'.format(time)
    elif len(str(time)) == 19:
        _time = str(time)
    else:
        QA_util_log_info('WRONG DATETIME FORMAT {}'.format(time))
    return datetime.datetime.strptime(_time, '%Y-%m-%d %H:%M:%S')


def QA_util_date_stamp(date):
    """[summary]
    
    Arguments:
        date {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    datestr = str(date)[0:10]
    date = time.mktime(time.strptime(datestr, '%Y-%m-%d'))
    return date


def QA_util_time_stamp(time_):
    '''
    数据格式最好是%Y-%m-%d %H:%M:%S 中间要有空格 
    '''
    if len(str(time_)) == 10:
        # yyyy-mm-dd格式
        return time.mktime(time.strptime(time_, '%Y-%m-%d'))
    elif len(str(time_)) == 16:
            # yyyy-mm-dd hh:mm格式
        return time.mktime(time.strptime(time_, '%Y-%m-%d %H:%M'))
    else:
        timestr = str(time_)[0:19]
        return time.mktime(time.strptime(timestr, '%Y-%m-%d %H:%M:%S'))


def QA_util_stamp2datetime(timestamp):
    """
    datestamp转datetime

    pandas转出来的timestamp是13位整数 要/1000

    """
    try:
        return datetime.datetime.fromtimestamp(timestamp)
    except Exception as e:
        return datetime.datetime.fromtimestamp(timestamp / 1000)


def QA_util_ms_stamp(ms):
    """[summary]
    
    Arguments:
        ms {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    return ms


def QA_util_date_valid(date):
    """[summary]
    
    Arguments:
        date {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    try:

        time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False


def QA_util_realtime(strtime, client):
    """[summary]
    
    Arguments:
        strtime {[type]} -- [description]
        client {[type]} -- [description]
    """

    time_stamp = QA_util_date_stamp(strtime)
    coll = client.quantaxis.trade_date
    temp_str = coll.find_one({'date_stamp': {"$gte": time_stamp}})
    time_real = temp_str['date']
    time_id = temp_str['num']
    return {'time_real': time_real, 'id': time_id}


def QA_util_id2date(idx, client):
    """[summary]
    
    Arguments:
        idx {[type]} -- [description]
        client {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    coll = client.quantaxis.trade_date
    temp_str = coll.find_one({'num': idx})
    return temp_str['date']


def QA_util_is_trade(date, code, client):
    """判断是否是交易日
    
    Arguments:
        date {[type]} -- [description]
        code {[type]} -- [description]
        client {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    coll = client.quantaxis.stock_day
    date = str(date)[0:10]
    is_trade = coll.find_one({'code': code, 'date': date})
    try:
        len(is_trade)
        return True
    except:
        return False


def QA_util_get_date_index(date, trade_list):
    """返回在trade_list中的index位置
    
    Arguments:
        date {[type]} -- [description]
        trade_list {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    return trade_list.index(date)


def QA_util_get_index_date(id, trade_list):
    return trade_list[id]


def QA_util_select_hours(time=None, gt=None, lt=None, gte=None, lte=None):
    'quantaxis的时间选择函数,约定时间的范围,比如早上9点到11点'
    if time is None:
        __realtime = datetime.datetime.now()
    else:
        __realtime = time

    fun_list = []
    if gt != None:
        fun_list.append('>')
    if lt != None:
        fun_list.append('<')
    if gte != None:
        fun_list.append('>=')
    if lte != None:
        fun_list.append('<=')

    assert len(fun_list) > 0
    true_list = []
    try:
        for item in fun_list:
            if item == '>':
                if __realtime.strftime('%H') > gt:
                    true_list.append(0)
                else:
                    true_list.append(1)
            elif item == '<':
                if __realtime.strftime('%H') < lt:
                    true_list.append(0)
                else:
                    true_list.append(1)
            elif item == '>=':
                if __realtime.strftime('%H') >= gte:
                    true_list.append(0)
                else:
                    true_list.append(1)
            elif item == '<=':
                if __realtime.strftime('%H') <= lte:
                    true_list.append(0)
                else:
                    true_list.append(1)

    except:
        return Exception
    if sum(true_list) > 0:
        return False
    else:
        return True


def QA_util_select_min(time=None, gt=None, lt=None, gte=None, lte=None):
    'quantaxis的时间选择函数,约定时间的范围,比如30分到59分'
    if time is None:
        __realtime = datetime.datetime.now()
    else:
        __realtime = time

    fun_list = []
    if gt != None:
        fun_list.append('>')
    if lt != None:
        fun_list.append('<')
    if gte != None:
        fun_list.append('>=')
    if lte != None:
        fun_list.append('<=')

    assert len(fun_list) > 0
    true_list = []
    try:
        for item in fun_list:
            if item == '>':
                if __realtime.strftime('%M') > gt:
                    true_list.append(0)
                else:
                    true_list.append(1)
            elif item == '<':
                if __realtime.strftime('%M') < lt:
                    true_list.append(0)
                else:
                    true_list.append(1)
            elif item == '>=':
                if __realtime.strftime('%M') >= gte:
                    true_list.append(0)
                else:
                    true_list.append(1)
            elif item == '<=':
                if __realtime.strftime('%M') <= lte:
                    true_list.append(0)
                else:
                    true_list.append(1)

    except:
        return Exception
    if sum(true_list) > 0:
        return False
    else:
        return True


def QA_util_time_delay(time_=0):
    '这是一个用于复用/比如说@装饰器的延时函数\
    使用threading里面的延时,为了是不阻塞进程\
    有时候,同时发进去两个函数,第一个函数需要延时\
    第二个不需要的话,用sleep就会阻塞掉第二个进程'
    def _exec(func):
        threading.Timer(time_, func)
    return _exec


def QA_util_calc_time(func, *args, **kwargs):
    '耗时长度的装饰器'
    _time = datetime.datetime.now()
    func(*args, **kwargs)
    print(datetime.datetime.now() - _time)
    # return datetime.datetime.now() - _time


if __name__ == '__main__':
    print(QA_util_time_stamp('2017-01-01 10:25:08'))
