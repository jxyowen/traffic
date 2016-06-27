__author__ = 'jxy'
from rest_framework import permissions


class IsAuthenticatedOrNotPost(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """
    def has_permission(self, request, view):
        return (
            (request.method != 'POST') or
            request.user and
            request.user.is_authenticated()
        )

