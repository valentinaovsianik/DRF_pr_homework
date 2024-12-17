from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """Проверяет, входит ли пользователь в группу модераторов"""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name="Moderator").exists()


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем курса"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
