from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """Проверяет, входит ли пользователь в группу модераторов"""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name="Moderator").exists()


class IsNotModerator(permissions.BasePermission):
    """Запрещает доступ модераторам для определенных действий."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return True
        return not request.user.groups.filter(name="Moderator").exists()
