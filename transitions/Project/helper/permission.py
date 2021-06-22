from django.contrib.auth.models import Permission, User
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user == "Fadhel")


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user == "genji")


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user == "customer")

class IsPermission(BasePermission):
    def has_permission(self, request, view):
        print("entry perm")
        path = {"/api/sendwhatsappnotemplate/": "message", "/api//sendsmsnotemplate": "message",
                "/api/sendwhatsapp/": "message",
                "/api/sendsms/": "message", "/api/sendemail/": "email", "/api/Log/": "log",
                "/api/template/": "template"}
        method = {"GET": "view", "POST": "add", "PUT": "change"}
        tt = path[request.META["PATH_INFO"]]
        get = Permission.objects.filter(codename__contains=method[request.method], codename__icontains=tt).values('codename')[0]['codename']
        print(User.objects.get(username="Fadhel").id)
        print(Permission.objects.filter(user=User.objects.get(username="Fadhel").id))
        if request.user.has_perm("Project." + get):
            return True
        return False

