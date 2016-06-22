from rest_framework import permissions

GENERATOR_METHODS = ('GET', 'HEAD', 'OPTIONS', 'PUT', 'DELETE')

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in GENERATOR_METHODS:
            return True
        return False
        # Write permissions are only allowed to the owner of the snippet.
        # return obj.owner == request.user