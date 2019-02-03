
from rest_framework.permissions import BasePermission


class IsWorker(BasePermission):
    def has_permission(self, request, view):
        return (request.user is not None) & hasattr(request.user, "worker")


class IsCompany(BasePermission):
    def has_permission(self, request, view):
        return (request.user is not None) & hasattr(request.user, "company")


class CustomDictPermission(BasePermission):

    # set {key, [method, method,...]}
    SAFE_PETTERN = {}

    def has_permission(self, request, view):
        if request.user is None:
            return False

        for key, values in self.SAFE_PETTERN.items():
            if hasattr(request.user, key):
                if request.method in values:
                    return True
        return False
