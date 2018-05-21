#coding:utf-8
import json
from django.http import HttpResponse, HttpResponseRedirect
from admin import admin_service
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, render
# Create your views here.

# 定时数据整理
from apscheduler.schedulers.background import BackgroundScheduler
update_data_sch = BackgroundScheduler()
update_data_sch.add_job(admin_service.update_stock_data, "interval", hours=2)
update_data_sch.add_job(admin_service.start_select_stock, "interval", hours=4)
update_data_sch.start()

def login(request):
    return render_to_response("login.html")

def logout(request):
    response = HttpResponseRedirect('/admin/login/')
    response.delete_cookie('username')
    return response

def data_manage(request):
    return render_to_response("admin_data_manage.html")

def admin_home(request):
    resp = admin_service.get_terminals()
    mac_list = []
    for item in resp:
        mac_list.append(item["mac"])
    mac_list = enumerate(mac_list)
    return render(request, "admin_home.html", {"mac_list": mac_list})

@csrf_exempt
def do_login(request):
    if request.method == "POST":
        # body_json = json.loads(request.body)
        username = request.POST.get("username"," ")
        password = request.POST.get("password", " ")
    else:
        resp = {"result": "failed"}
        return HttpResponse(json.dumps(resp))
    resp = admin_service.check_user(username, password)
    response = HttpResponse(json.dumps(resp))
    if (resp["result"] == "success"):
        print("set cookie")
        response.set_cookie("username",admin_service.get_admin_name())
    return response

def get_admin_name(request):
    resp = admin_service.get_admin_name()
    response = HttpResponse(json.dumps(resp))
    return response

def add_terminal(request):
    """
    添加终端
    :param request:
    :return:
    """
    if request.method == "POST":
        mac_addr = request.POST.get("mac_terminal"," ")
    else:
        return HttpResponse()
    resp = admin_service.add_terminal(mac_addr)
    response = HttpResponse(json.dumps(resp))
    return response

def get_terminals(request):
    """
    获取所有终端
    :param request:
    :return:
    """
    resp = admin_service.get_terminals()
    response = HttpResponse(json.dumps(resp))
    return response

def delete_terminal(request):
    """
    删除终端
    :param request:
    :return:
    """
    if request.method == "POST":
        mac_addr = request.POST.get("mac_terminal"," ")
    else:
        return HttpResponse()
    resp = admin_service.delete_terminal(mac_addr)
    response = HttpResponse(json.dumps(resp))
    return response

def update_stock_data(request):
    """
    更新股票数据
    :param request:
    :return:
    """
    resp = admin_service.update_stock_data()
    response = HttpResponse(json.dumps(resp))
    return response

def get_update_progress(request):
    """
    获取进度条
    :param request:
    :return:
    """
    resp = admin_service.get_update_progress()
    response = HttpResponse(json.dumps(resp))
    return response

def start_select_stock(request):
    resp = admin_service.start_select_stock()
    response = HttpResponse(json.dumps(resp))
    return response

def get_latest_select_date(request):
    resp = admin_service.get_last_select_date()
    response = HttpResponse(json.dumps(resp))
    return response

def get_select_result(request):
    mac_addr = request.COOKIES.get("mac_addr", "")
    date = request.GET.get("T2Date", "")
    resp = admin_service.get_select_result(date, mac_addr)
    response = HttpResponse(json.dumps(resp))
    return response