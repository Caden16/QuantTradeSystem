# coding=utf-8
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


from ..QAUtil.QALogs import QA_util_log_info


def QA_user_sign_in(name, password, client):
    coll = client.quantaxis.user_list
    cursor=coll.find({'username': name, 'password': password})
    if (cursor.count() > 0):
        QA_util_log_info('success login! your username is:' + str(name))
        return cursor
    else:
        QA_util_log_info('Failed to login,please check your password ')
        return None


def QA_user_sign_up(name, password, client):
    coll = client.quantaxis.user_list
    if (coll.find({'username': name}).count() > 0):
        QA_util_log_info('user name is already exist')
        return False
    else:
        coll.insert({'username': name, 'password': password})
        QA_util_log_info('Success sign in! please login ')
        return True
