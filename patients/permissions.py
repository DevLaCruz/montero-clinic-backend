from rest_framework import permissions

class IsNotStaff(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a los usuarios que no son staff (is_staff=False).
    """

    def has_permission(self, request, view):
        # Permitir solo si el usuario está autenticado y no es staff
        return request.user.is_authenticated and not request.user.is_staff