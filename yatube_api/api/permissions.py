from rest_framework import permissions
from rest_framework.permissions import BasePermission


class AllowAnyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user == obj.author)


class IsGetRequest(BasePermission):
    def has_permission(self, request, view):
        # Разрешить GET-запросы
        if not request.user.is_authenticated:
            return request.method == 'GET'
        return True
