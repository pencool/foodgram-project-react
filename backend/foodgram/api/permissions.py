from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Права доступа: администратор или чтение"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))


class IsAdminPermission(permissions.BasePermission):
    """ Права доступа: Администратор."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)


class IsOwnerOrReadOnlyPermission(permissions.IsAuthenticatedOrReadOnly):
    """Права доступа: автор или чтение."""

    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS
                or obj.author == request.user
        )
