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


from ..QASU.user import QA_user_sign_in
from ..QAUtil.QASql import QA_util_sql_mongo_setting


class QA_Setting():
    def __init__(self, ip='127.0.0.1', port=27017):
        self.ip = ip
        self.port = port
        self.username = None
        self.password = None

    @property
    def client(self):
        return QA_util_sql_mongo_setting(self.ip, self.port)

    def change(self, ip, port):
        self.ip = ip
        self.port = port
        global DATABASE
        DATABASE = self.client.quantaxis
        return self

    def login(self, user_name, password):
        user = QA_user_sign_in(user_name, password, self.client)
        if user is not None:
            self.user_name = user_name
            self.password = password
            self.user = user
            return self.user
        else:
            return False


DATABASE = QA_Setting().client.quantTradeSystemDB


info_ip_list = ['101.227.73.20', '101.227.77.254',
                '114.80.63.12', '114.80.63.35',
                '115.238.56.198', '115.238.90.165',
                '124.160.88.183', '60.28.23.80',
                '14.215.128.18', '180.153.18.170',
                '180.153.18.171',
                '180.153.39.51', '202.108.253.130',
                '202.108.253.131',
                '218.108.47.69', '218.108.98.244',
                '218.75.126.9',
                '221.231.141.60',
                '59.173.18.140',
                '60.12.136.250', ]


stock_ip_list = ['218.85.139.19','tdx.xmzq.com.cn',
                 '218.75.126.9', '115.238.90.165',
                 '124.160.88.183', '60.12.136.250',
                 '218.108.98.244', '218.108.47.69',
                 '180.153.39.51', '121.14.2.7',
                 '180.153.18.170','180.153.18.171',
                 '61.135.142.73', '115.238.56.198',
                 '60.191.117.167', 'hq.cjis.cn',
                 '59.173.18.69', 'sztdx.gtjas.com',
                 'jstdx.gtjas.com', 'shtdx.gtjas.com',
                 '218.9.148.108', '61.153.144.179',
                 'hq1.daton.com.cn']

future_ip_list = ['61.152.107.141']


"""
['121.14.110.210', '119.147.212.76', '113.105.73.86', '119.147.171.211', '119.147.164.57', '119.147.164.58', '61.49.50.180', '61.49.50.181',
'61.135.142.85', '61.135.149.181', '114.80.80.210', '222.73.49.15', '221.194.181.176']
"""
