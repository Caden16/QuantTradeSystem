#coding: utf-8
import datetime
import threading
import json
from multiprocessing import Pool, Manager

import os
from dataSort.QASU.main import *

PROGRESS_INFO = {}
PROGRESS_INFO_FILE = os.path.dirname(__file__) + os.sep + "PROGRESS_INFO.json"
def start_update_stock_data():
    print("start_update_stock_data")
    global PROGRESS_INFO
    if PROGRESS_INFO.get("stock_day_total", 0) > 0 and PROGRESS_INFO.get("xdxr_total", 0) > 0 and \
            (PROGRESS_INFO["stock_day_num"] < PROGRESS_INFO["stock_day_total"] or
             PROGRESS_INFO["xdxr_num"] < PROGRESS_INFO["xdxr_total"]):
        return
    manage = Manager()
    PROGRESS_INFO = manage.dict()
    PROGRESS_INFO.clear()
    PROGRESS_INFO["save_date"] = get_last_index_date()
    PROGRESS_INFO["stock_day_num"] = 0
    PROGRESS_INFO["stock_day_total"] = 0
    PROGRESS_INFO["xdxr_num"] = 0
    PROGRESS_INFO["xdxr_total"] = 0
    pool = Pool(4)
    pool.apply_async(save_progress_data_to_file, (PROGRESS_INFO,))
    # save_progress_data_to_file()
    # QA_SU_save_stock_list('tdx')
    # QA_SU_save_stock_day('tdx', PROGRESS_INFO=PROGRESS_INFO)
    pool.apply_async(QA_SU_save_stock_day, ('tdx', PROGRESS_INFO))
    # QA_SU_save_stock_xdxr('tdx', PROGRESS_INFO=PROGRESS_INFO)
    pool.apply_async(QA_SU_save_stock_xdxr, ('tdx', PROGRESS_INFO))
    pool.close()
    pool.join()
    QA_SU_save_index_day('tdx')
    PROGRESS_INFO["save_date"] = get_last_index_date()
    # save_progress_data_to_file()
    json.dump(dict(PROGRESS_INFO), open(PROGRESS_INFO_FILE, "w"))
    PROGRESS_INFO.clear()
    return


def get_update_progress():
    global PROGRESS_INFO
    temp_dict = dict(PROGRESS_INFO)
    if len(temp_dict) > 0:
        return temp_dict
    else:
        if not os.path.exists(PROGRESS_INFO_FILE):
            return None
        temp_dict = json.load(open(PROGRESS_INFO_FILE))
        return temp_dict


def get_last_index_date():
    index_day_collection = DATABASE.index_day
    index_day_data = index_day_collection.find({"code": "000001"})
    if index_day_data is None or index_day_data.count() <= 0:
        return datetime.datetime.now().strftime('%Y-%m-%d')
    date = index_day_data[index_day_data.count() - 1]["date"]
    return date

def save_progress_data_to_file(PROGRESS_INFO):
    global PROGRESS_INFO_FILE
    global progress_timer
    temp_dict = dict(PROGRESS_INFO)
    if len(temp_dict) > 0:
        json.dump(temp_dict, open(PROGRESS_INFO_FILE, "w"))
        print("dump")
        progress_timer = threading.Timer(1, save_progress_data_to_file, args=(PROGRESS_INFO,))
        progress_timer.start()
        # progress_timer.join()
    else:
        print("progress_timer cancel")
        progress_timer.cancel()
        progress_timer = None
        return