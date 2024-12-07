from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedUMKT(BasePermission):
    """
    Allows access only to valid users.
    """

    def has_permission(self, request, view):
        return bool(request.user_umkt)


class IsAdminUserUMKT(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user_umkt and request.user_umkt.is_staff)


class IsAuthenticatedOrReadOnlyUMKT(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user_umkt
        )


class IsMahasiswaUMKT(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user_umkt and request.user_umkt[0].is_digit())


class IsPegawaiOrDosenUMKT(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user_umkt and not request.user_umkt[0].is_digit())
