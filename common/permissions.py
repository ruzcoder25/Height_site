from rest_framework.permissions import BasePermission, SAFE_METHODS

from account.models import RoleChoices


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')

class IsModeratorOrAdmin(BasePermission):
    message = "Faqat moderator yoki administrator ruxsatiga ega."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in [RoleChoices.MODERATOR, RoleChoices.ADMIN]
        )

# class IsAdminOrIsSelf(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.user.is_authenticated and request.user.role == 'admin':
#             return True
#         return obj == request.user


