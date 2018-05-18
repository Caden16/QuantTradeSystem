from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
import admin.views as admin_view

urlpatterns = [
    url(r'^admin/login', admin_view.login),
    url(r'^admin/home', admin_view.admin_home),
    url(r'^admin/data_manage', admin_view.data_manage),
    url(r'^api/admin/login', admin_view.do_login),
    url(r'^api/admin/logout', admin_view.logout),
    url(r'^api/admin/get_admin_name', admin_view.get_admin_name),
    url(r'^api/admin/add_terminal', admin_view.add_terminal),
    url(r'^api/admin/get_terminals', admin_view.get_terminals),
    url(r'^api/admin/delete_terminal', admin_view.delete_terminal),
    url(r'^api/admin/update_stock_data', admin_view.update_stock_data),
    url(r'^api/admin/get_update_progress', admin_view.get_update_progress),
    url(r'^api/admin/start_select_stock', admin_view.start_select_stock),
    url(r'^api/admin/get_latest_select_date', admin_view.get_latest_select_date),
    url(r'^api/admin/get_select_result', admin_view.get_select_result)
]

urlpatterns += staticfiles_urlpatterns()
