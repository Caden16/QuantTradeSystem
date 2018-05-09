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
""""
yutiansut
util tool
"""


# bar
from ..QAUtil.QABar import (QA_util_make_hour_index,
                                    QA_util_make_min_index, QA_util_time_gap)
# config
from ..QAUtil.QACfg import QA_util_cfg_initial, QA_util_get_cfg
# csv
from ..QAUtil.QACsv import QA_util_save_csv
# date
from ..QAUtil.QADate import (QA_util_date_int2str, QA_util_date_stamp,
                                     QA_util_date_str2int, QA_util_date_today,
                                     QA_util_date_valid, QA_util_calc_time,
                                     QA_util_get_date_index, QA_util_to_datetime,
                                     QA_util_get_index_date, QA_util_id2date,
                                     QA_util_is_trade, QA_util_ms_stamp,
                                     QA_util_realtime, QA_util_select_hours,
                                     QA_util_select_min, QA_util_time_delay,
                                     QA_util_time_now, QA_util_time_stamp)
# trade date
from ..QAUtil.QADate_trade import (QA_util_date_gap,
                                           QA_util_get_real_date,
                                           QA_util_get_real_datelist,
                                           QA_util_get_trade_gap,
                                           QA_util_get_trade_range,
                                           QA_util_if_trade,
                                           QA_util_if_tradetime,
                                           QA_util_get_next_day,
                                           QA_util_get_last_day,
                                           trade_date_sse)
# list function
from ..QAUtil.QAList import (QA_util_diff_list,
                                     QA_util_multi_demension_list)

# code function
from ..QAUtil.QACode import QA_util_code_tostr
# dict function
from ..QAUtil.QADict import QA_util_dict_remove_key
# log
from ..QAUtil.QALogs import (QA_util_log_debug, QA_util_log_expection,
                                     QA_util_log_info)
# MongoDB
from ..QAUtil.QAMongo import (QA_util_mongo_infos,
                                      QA_util_mongo_initial,
                                      QA_util_mongo_status)
# Parameter
from ..QAUtil.QAParameter import (MARKET_TYPE, ORDER_STATUS, TRADE_STATUS, DATASOURCE, OUTPUT_FORMAT,
                                          ORDER_DIRECTION, ORDER_MODEL, ORDER_EVENT, FREQUENCE, BROKER_TYPE,
                                          ACCOUNT_EVENT, BROKER_EVENT, EVENT_TYPE, MARKET_EVENT, ENGINE_EVENT,
                                          RUNNING_ENVIRONMENT, AMOUNT_MODEL, MARKET_ERROR)
# RANDOM class
from ..QAUtil.QARandom import QA_util_random_with_topic
# QUANTAXIS Setting
from ..QAUtil.QASetting import (QA_Setting, DATABASE, future_ip_list,
                                        info_ip_list, stock_ip_list)
# sql
from ..QAUtil.QASql import (QA_util_sql_async_mongo_setting,
                                    QA_util_sql_mongo_setting,
                                    QA_util_sql_mongo_sort_ASCENDING,
                                    QA_util_sql_mongo_sort_DESCENDING)
# format
from ..QAUtil.QATransform import (QA_util_to_json_from_pandas,
                                          QA_util_to_list_from_numpy,
                                          QA_util_to_list_from_pandas,
                                          QA_util_to_pandas_from_json,
                                          QA_util_to_pandas_from_list)
# 网络相关
from ..QAUtil.QAWeb import QA_util_web_ping
from ..QAUtil.QAMail import QA_util_send_mail
