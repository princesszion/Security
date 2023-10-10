from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to allow access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user.role == 'team_lead'

class IsRegularUser(permissions.BasePermission):
    """
    Custom permission to allow access only to regular (non-admin) users.
    """
    def has_permission(self, request, view):
        return request.user.role == 'student'
