from rest_framework import permissions


class InviteUserEmailPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_company_admin
        )