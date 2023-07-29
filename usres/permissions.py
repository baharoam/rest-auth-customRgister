from rest_framework.permissions import BasePermission
from .models import Teacher

from rest_framework import permissions

class IsTeacherPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        print("role is", request.user.role)
        return request.user.is_authenticated and request.user.role == 'Teacher'

class IsStudentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        print("role is", request.user.role)
        return request.user.is_authenticated and request.user.role == 'Student'