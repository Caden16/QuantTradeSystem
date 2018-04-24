#coding: utf-8
from .utils import get_db_connection

def get_select_result(date_str):
    collections = get_db_connection()
    result_collection = collections.select_stock_result
    select_result = result_collection.find_one({"date": date_str})
    if select_result is None:
        return [{"date":"2018-04-06"},{"code":"000001"}]
    return select_result["date"]