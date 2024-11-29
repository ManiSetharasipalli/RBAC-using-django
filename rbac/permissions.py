from rest_framework.permissions import BasePermission

# Custom Permissions for roles

class IsAdmin(BasePermission):
    """
    Allows access only to users who are part of the 'Admin' group.
    """
    def has_permission(self, request, view):
        # Check if the user is part of the 'Admin' group
        return request.user.groups.filter(name='Admin').exists()

class IsModerator(BasePermission):
    """
    Allows access only to users who are part of the 'Moderator' group.
    """
    def has_permission(self, request, view):
        # Check if the user is part of the 'Moderator' group
        return request.user.groups.filter(name='Moderator').exists()

class IsUser(BasePermission):
    """
    Allows access only to users who are part of the 'User' group.
    """
    def has_permission(self, request, view):
        # Check if the user is part of the 'User' group
        return request.user.groups.filter(name='User').exists()
