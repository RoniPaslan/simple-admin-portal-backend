from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"

class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ["admin", "manager"]

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return request.user.role in ["admin", "manager"]
