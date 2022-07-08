from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsDoctorOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and (request.user.role == 'D' or request.user.is_staff))


class IsPrescriptionOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.patient == request.user or obj.doctor == request.user


class IsPrescriptionMedicineOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.prescription.patient == request.user or obj.prescription.doctor == request.user or request.user.is_staff
