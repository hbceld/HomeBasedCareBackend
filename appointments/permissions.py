from rest_framework import permissions

class IsAdminOrAssignedNurse(permissions.BasePermission):
    """
    Admins can see all appointments.
    Nurses can see only their assigned appointments.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True  # Admin sees all
        if hasattr(obj, "assigned_nurse") and obj.assigned_nurse == request.user:
            return True  # Nurse sees only assigned
        return False
