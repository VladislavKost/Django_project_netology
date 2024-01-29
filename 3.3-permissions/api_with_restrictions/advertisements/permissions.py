from rest_framework.permissions import BasePermission


class IsAdsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.pk == 1:
            return True
        return request.user == obj.creator
