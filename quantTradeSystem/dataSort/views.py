import json

from django.shortcuts import render
from django.http import HttpResponse
from .get_select_result_from_db import get_select_result
# Create your views here.

def select_result(request):
    date_str = request.GET["T2date"]
    print(date_str)
    select_result = get_select_result(date_str)
    resp = {"result": select_result}
    return HttpResponse(json.dumps(resp), content_type="application/json")