from rest_framework import permissions

class IsAdminOrAssignedNurse(permissions.BasePermission):
    """
    Admins can see all appointments.
    Nurses can see only their assigned appointments.
    Patients can see their own appointments.
    """

    def has_permission(self, request, view):
        # allow only authenticated users to access appointment endpoints at all
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Admin (staff or superuser) can access everything
        if request.user.is_staff or request.user.is_superuser:
            return True

        # Nurse: compare the underlying user on the NurseProfile
        if hasattr(obj, "assigned_nurse") and obj.assigned_nurse is not None:
            nurse_user = getattr(obj.assigned_nurse, "user", None)
            if nurse_user and nurse_user == request.user:
                return True

        # Patient: compare the patient profile's user
        if hasattr(obj, "patient") and obj.patient is not None:
            patient_user = getattr(obj.patient, "user", None)
            if patient_user and patient_user == request.user:
                return True

        return False

