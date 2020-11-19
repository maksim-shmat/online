""" Docs """

from rest_framework.permissions import BasePermission

class IsEnrolled(BasePermission):
    """ docs for class """
    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()
