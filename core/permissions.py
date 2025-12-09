from rest_framework import permissions


class IsManager(permissions.BasePermission):
    """Позволяет выполнять действие только менеджеру."""
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and user.groups.filter(name="Менеджер").exists()
        )


class IsServiceCompany(permissions.BasePermission):
    """Проверка для сервисной организации."""
    def has_permission(self, request, view):
        u = request.user
        return u.is_authenticated and u.groups.filter(name="Сервисная организация").exists()


class IsClient(permissions.BasePermission):
    """Проверка для клиента."""
    def has_permission(self, request, view):
        u = request.user
        return u.is_authenticated and u.groups.filter(name="Клиент").exists()


class CanCreateMaintenance(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.groups.filter(name="Менеджер").exists():
            return True

        if user.groups.filter(name="Клиент").exists():
            return obj.client == user

        if user.groups.filter(name="Сервисная организация").exists():
            return obj.service_company == user

        return False
