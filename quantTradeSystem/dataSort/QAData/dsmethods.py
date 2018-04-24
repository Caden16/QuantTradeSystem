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


"""DataStruct的方法
"""
import pandas as pd
from ..QAData.QADataStruct import QA_DataStruct_Stock_day, QA_DataStruct_Stock_min


def concat(lists):
    """类似于pd.concat 用于合并一个list里面的多个DataStruct,会自动去重



    Arguments:
        lists {[type]} -- [DataStruct1,DataStruct2,....,DataStructN]

    Returns:
        [type] -- new DataStruct
    """

    return lists[0].new(pd.concat([lists.data for lists in lists]).drop_duplicates())


def from_tushare(dataframe, dtype='day'):
    """dataframe from tushare
    
    Arguments:
        dataframe {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    if dtype in ['day']:
        return QA_DataStruct_Stock_day(dataframe.set_index(['date', 'code'], drop=False), dtype='stock_day')
    elif dtype in ['min']:
        return QA_DataStruct_Stock_min(dataframe.set_index(['datetime', 'code'], drop=False), dtype='stock_min')


