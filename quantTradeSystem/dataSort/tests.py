from django.test import TestCase

# Create your tests here.
from quantTradeSystem.dataSort.QAFetch.QAQuery_Advance import QA_fetch_stock_day_adv
from quantTradeSystem.dataSort.QASU.main import *

# if __name__ == '__main__':
# QA_SU_save_stock_day('tdx')
# testdf = QA_fetch_stock_day_adv("000001").to_qfq()
# QA_SU_save_stock_xdxr('tdx')
QA_SU_save_index_day('tdx')
# QA_SU_save_stock_list('tdx')
# print(testdf.close)