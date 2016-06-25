from rest_framework import permissions


class CRUDWithoutAuthentication(permissions.BasePermission):

    """
    POST,PUT permissions for updatinng/creating data
    """

    def has_permission(self, request, view):

        allowed_methods = ['POST', 'PUT', 'DELETE']
        if (request.method in allowed_methods):
            return True
        return False
