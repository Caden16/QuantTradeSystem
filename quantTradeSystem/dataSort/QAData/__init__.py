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

from ..QAData.data_fq import (QA_data_get_hfq, QA_data_get_qfq,
                                      QA_data_make_hfq, QA_data_make_qfq,
                                      QA_data_stock_to_fq)
from ..QAData.data_resample import QA_data_tick_resample
from ..QAData.QADataStruct import (QA_DataStruct_Index_day,
                                           QA_DataStruct_Index_min,
                                           QA_DataStruct_Stock_block,
                                           QA_DataStruct_Stock_day,
                                           QA_DataStruct_Stock_min,
                                           QA_DataStruct_Future_day,
                                           QA_DataStruct_Future_min,
                                           QA_DataStruct_Stock_transaction)
