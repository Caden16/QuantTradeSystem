from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x


class SimpleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == "/admin/login" or request.path.find("/api/admin/login") >= 0 or \
                request.path.find("api/admin/get_select_result") >= 0:
            return
        user = request.COOKIES.get("username", "")
        if not user:
            print("redirect " + user)
            return redirect("/admin/login")
