#encoding: utf-8
import json

import time
import tushare as ts
import pymongo

from multiprocessing import Pool

"""
    从tushare导入数据到mongodb
"""
class ImportDataFromTushare():

    @classmethod
    def __init__(self):
        self.mongo_connect = pymongo.MongoClient("127.0.0.1", port=27017)
        self.db = self.mongo_connect["quantTradeSystemDB"]
        self.stock_day_collection = self.db.stock_day_data

    @classmethod
    def parse_df_to_dict(cls, temp_df):
        if temp_df is None:
            return {}
        one_stock_data_df = temp_df.reset_index(drop=True)
        if "code" in one_stock_data_df.columns:
            one_stock_data_df = one_stock_data_df.drop(["code"], axis=1)
        one_stock_data_dict = one_stock_data_df.to_json(orient="records")
        return one_stock_data_dict

    @classmethod
    def import_day_data(cls, stock_code, start_date, end_date):
        one_stock_data_df = ts.get_k_data(code=stock_code, ktype="D", autype="qfq", start=start_date, end=end_date)
        one_stock_data_dict = cls.parse_df_to_dict(one_stock_data_df)
        one_stock_data ={"stock_code": stock_code, "day_data": json.loads(one_stock_data_dict)}
        cls.stock_day_collection.insert(one_stock_data)

    @classmethod
    def get_day_data_from_db(cls, stock_code):
        one_code_data = cls.stock_day_collection.find_one({"stock_code": stock_code})
        db_day_data = one_code_data["day_data"]
        if db_day_data is None:
            return []
        return one_code_data

    @classmethod
    def update_day_data(cls, stock_code, start_date, end_date):
        one_stock_data_df = ts.get_k_data(code=stock_code, ktype="D", autype="qfq", start=start_date, end=end_date)
        one_stock_data_dict = cls.parse_df_to_dict(one_stock_data_df)
        if not one_stock_data_dict:
            return
        one_code_db_data = cls.get_day_data_from_db(stock_code)
        one_code_db_data.append(one_stock_data_dict)
        cls.stock_day_collection.update({"stock_code": stock_code}, {"day_data": one_code_db_data})


if __name__ == '__main__':
    stock_basic = ts.get_stock_basics()
    all_stock_list = list(stock_basic.index)
    all_stock_list.sort()
    run_pool = Pool(6)
    start_date = "2014-01-01"
    end_date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    import_data_obj = ImportDataFromTushare()
    for code in all_stock_list:
        if code < "300741":
            continue
        # run_pool.apply_async(import_data_obj.import_day_data, args=(code,start_date, end_date))
        import_data_obj.import_day_data(code, start_date, end_date)
    run_pool.close()
    run_pool.join()
    print("导入完成")

