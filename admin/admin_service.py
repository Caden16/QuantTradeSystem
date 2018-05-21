#coding: utf-8
import re

import os

from admin import admin_dao
from dataSort import data_sort_service_main
from multiprocessing import Process
from selectStock.select import select_base

run_process = None
select_process = None
def check_user(username, password):
    if not (username and password):
        login_result = "failed"
        resp = {"result": login_result, "message": "密码错误"}
        return resp

    check_result = admin_dao.check_user(username, password)
    if check_result:
        login_result = "success"
        resp = {"result": login_result, "message": "登录成功"}
    else:
        login_result = "failed"
        resp = {"result": login_result, "message": "密码错误"}
    return resp

def get_admin_name():
    username = admin_dao.get_admin_name()
    resp = {"username": username}
    return resp

def valid_mac_num(mac_addr):
    if not mac_addr:
        return False
    if re.match(r"^\s*([0-9a-fA-F]{2,2}-){5,5}[0-9a-fA-F]{2,2}\s*$", mac_addr):
        return True
    return False

def add_terminal(mac_addr):
    resp = {}
    if not valid_mac_num(mac_addr):
        resp["result"] = "failed"
        resp["message"] = "非法MAC地址"
        return resp
    admin_dao.add_terminal(mac_addr)
    resp["result"] = "success"
    return resp

def get_terminals():
    resp = admin_dao.get_terminals()
    return resp

def delete_terminal(mac_addr):
    resp = {}
    if not valid_mac_num(mac_addr):
        resp["result"] = "failed"
        resp["message"] = "非法MAC地址"
        return resp
    admin_dao.delete_terminal(mac_addr)
    resp["result"] = "success"
    return resp

def update_stock_data():
    global run_process
    resp = {"result": "success"}
    resp["message"] = ""
    if not run_process:
        if os.path.exists(data_sort_service_main.PROGRESS_INFO_FILE):
            os.remove(data_sort_service_main.PROGRESS_INFO_FILE)
        print("not run_process new process =========== ")
        run_process = Process(target=data_sort_service_main.start_update_stock_data)
        run_process.start()
        resp["message"] = "run_process new "
    if run_process.is_alive():
        print("is alive")
        resp["message"] += "old Process alive"
        return resp
    else:
        if data_sort_service_main.need_to_update_stock_data_check():
            if os.path.exists(data_sort_service_main.PROGRESS_INFO_FILE):
                os.remove(data_sort_service_main.PROGRESS_INFO_FILE)
        print("new Process alive")
        run_process = Process(target=data_sort_service_main.start_update_stock_data)
        run_process.start()
        resp["message"] += "new Process"
    return resp

def get_update_progress():
    result = data_sort_service_main.get_update_progress()
    resp = {}
    if not result:
        resp["result"] = "failed"
        resp["message"] = "进度不存在, 请先更新股票数据"
    else:
        resp["result"] = "success"
        resp["data"] = result
    return resp

def start_select_stock():
    global select_process
    resp = {"result": "success"}
    resp["message"] = ""
    if not select_process:
        select_process = Process(target=select_base.start_select_stock)
        select_process.start()
        resp["message"] = "run_process new "
    if select_process.is_alive():
        print("is alive")
        resp["message"] += "old Process alive"
        return resp
    else:
        print("new Process alive")
        select_process = Process(target=select_base.start_select_stock)
        select_process.start()
        resp["message"] += "new Process"
    return resp

def get_last_select_date():
    date = select_base.get_last_select_date()
    resp = {}
    if date:
        resp["result"] = "success"
        resp["last_select_date"] = date
    else:
        resp["result"] = "failed"
    return resp

def get_select_result(date, mac_addr=None, code=None):
    resp = {}
    mac_list = mac_addr.split(",")
    valid_mac = False
    for mac_item in mac_list:
        if check_mac_addr(mac_item):
            valid_mac = True
            break
    if not valid_mac:
        resp["result"] = "failed"
        resp["message"] = "invalid mac address"
        return resp
    select_result = None
    if date:
        select_result = select_base.get_select_result(date, code)

    if select_result:
        resp["result"] = "success"
        resp["data"] = select_result
    else:
        resp["result"] = "failed"
        resp["message"] = "T2Date contains 0 select result"
    return resp

def check_mac_addr(mac_addr):
    if not valid_mac_num(mac_addr):
        return True
    return admin_dao.check_terminal(mac_addr)