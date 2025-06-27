from rest_framework import permissions


class IsProjectOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners to edit/delete projects.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return (
                obj.owner == request.user
                or obj.members.filter(id=request.user.id).exists()
            )

        return obj.owner == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow read access to all authenticated users,
    but only allow write access to admin users.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # Write permissions are only allowed to admin users
        return request.user.is_authenticated and request.user.is_admin
