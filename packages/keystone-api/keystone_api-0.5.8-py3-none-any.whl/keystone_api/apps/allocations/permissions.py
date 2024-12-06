"""Custom permission objects used to manage access to HTTP endpoints.

Permission classes control access to API resources by determining user
privileges for different HTTP operations. They are applied at the view level,
enabling authentication and authorization to secure endpoints based on
predefined access rules.
"""

from rest_framework import permissions

from apps.users.models import Team
from .models import TeamModelInterface

__all__ = [
    'StaffWriteAuthenticatedRead',
    'StaffWriteMemberRead',
    'TeamAdminCreateMemberRead',
]


class TeamAdminCreateMemberRead(permissions.BasePermission):
    """Grant record creation permissions to team administrators and read permissions to all team members.

    Staff users retain all read/write permissions.
    """

    def has_permission(self, request, view) -> bool:
        """Return whether the request has permissions to access the requested resource."""

        # Staff users are OK. Read operations are also OK.
        if request.user.is_staff or request.method in permissions.SAFE_METHODS:
            return True

        # To check write permissions we need to know what team the record belongs to.
        # Deny permissions if the team is not provided or does not exist.
        try:
            team_id = request.data.get('team', None)
            team = Team.objects.get(pk=team_id)

        except (Team.DoesNotExist, Exception):
            return False

        return request.user in team.get_privileged_members()

    def has_object_permission(self, request, view, obj: TeamModelInterface) -> bool:
        """Return whether the incoming HTTP request has permission to access a database record."""

        is_staff = request.user.is_staff
        is_team_member = request.user in obj.get_team().get_all_members()

        if request.method in permissions.SAFE_METHODS:
            return is_team_member or is_staff

        return is_staff


class StaffWriteAuthenticatedRead(permissions.BasePermission):
    """Grant read-only access is granted to all authenticated users.

    Staff users retain all read/write permissions.
    """

    def has_permission(self, request, view) -> bool:
        """Return whether the request has permissions to access the requested resource."""

        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        return request.user.is_staff


class StaffWriteMemberRead(permissions.BasePermission):
    """Grant read access to users in to the same team as the requested object.

    Staff users retain all read/write permissions.
    """

    def has_permission(self, request, view) -> bool:
        """Return whether the request has permissions to access the requested resource."""

        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        return request.user.is_staff

    def has_object_permission(self, request, view, obj: TeamModelInterface) -> bool:
        """Return whether the incoming HTTP request has permission to access a database record."""

        if request.user.is_staff:
            return True

        user_is_in_team = request.user in obj.get_team().get_all_members()
        return request.method in permissions.SAFE_METHODS and user_is_in_team
