from django.conf.urls import url, include
from django.contrib import admin
from dataSort import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^', include('api.urls')),
    url(r'^select_result', views.select_result)
]