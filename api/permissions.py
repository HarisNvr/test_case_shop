from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.user.is_active

        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated
            and obj.author == request.user
        )
