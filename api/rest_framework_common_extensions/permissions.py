__author__ = 'jxy'
from rest_framework import permissions


class IsAuthenticatedOrNotPostDelete(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """
    def has_permission(self, request, view):
        return (
            (request.method not in ['POST', 'DELETE']) or
            request.user and
            request.user.is_authenticated()
        )

