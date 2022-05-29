from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsDoctorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        # return bool(request.user and request.user.role == 'D')


# TODO: IsPrescriptionOfOwnerDoctor
class IsPrescriptionOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.patient == request.user or obj.doctor == request.user
