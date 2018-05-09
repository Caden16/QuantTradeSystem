#coding:utf-8
import datetime

from quantTradeSystem.dataSort.QAUtil import DATABASE

import pandas as pd

def save_select_result(select_result, code=None):
    select_result_collection = DATABASE.select_stock_result
    date = select_result[0]["date"]
    exist_result_cursor = get_select_result(date, code)
    exist_result = []
    for item in exist_result_cursor:
        exist_result.append(item)
    if exist_result is not None and len(exist_result) >= 1:
        select_result = merge_select_result(select_result, exist_result, code)
    if code:
        select_result_collection.remove({"date": date, "code": code}, {"justOne": False})
    else:
        select_result_collection.remove({"date": date}, {"justOne": False})
    if len(select_result) == 0:
        return
    if len(select_result) > 1:
        select_result = list(select_result)
        select_result_collection.insert_many(select_result)
    else:
        select_result_collection.insert_one(select_result[0])

def get_select_result(date, code=None):
    select_result_collection = DATABASE.select_stock_result
    if code is None:
        return select_result_collection.find({"date": date})
    else:
        return select_result_collection.find({"date": date, "code": code})

def merge_select_result(result1, result2, code):
    """
    合并同一天的选股结果
    :param result1:
    :param result2:
    :return:
    """
    merge_result = []
    result2_df = pd.DataFrame(result2)
    for result_dict in result1:
        exist_code = result_dict.get("code")
        para_dict = result_dict.get("parameter")
        same_df = result2_df[result2_df["code"] == exist_code]
        if len(same_df) >= 1:
            result2_para = same_df["parameter"]
            para_dict = para_dict + result2_para
            result_dict["parameter"] = para_dict
            if code:
                return [result_dict]
        # merge_result.append(result_dict)
        result2_df = result2_df[result2_df["code"] != exist_code]
    result2_rest = result2_df.to_dict("records")
    merge_result = merge_result + result2_rest
    return merge_result

def get_last_index_date():
    index_day_collection = DATABASE.index_day
    index_day_data = index_day_collection.find({"code": "000001"})
    if index_day_data is None or index_day_data.count() <= 0:
        return datetime.datetime.now().strftime('%Y-%m-%d')
    date = index_day_data[index_day_data.count() - 1]["date"]
    return date