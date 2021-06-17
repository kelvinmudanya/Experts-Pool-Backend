from rest_framework import permissions


class AnonCreateAndUpdateOwnerOnly(permissions.BasePermission):
    """
    Custom permission:
        - allow anonymous POST
        - allow authenticated GET and PUT on *own* record
        - allow all actions for staff
    """

    def has_permission(self, request, view):
        return view.action == 'create' or request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return view.action in ['retrieve', 'update', 'partial_update'] and obj.id == request.user.id or request.user.is_staff


class ProfileAuthenticatedCreateAndUpdateOwnerOnly(permissions.BasePermission):
    """
    Custom permission:
        - allow anonymous POST
        - allow authenticated GET and PUT on *own* record
        - allow all actions for staff
    """

    def has_permission(self, request, view):
        return view.action == 'retrieve' and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return view.action in ['update', 'partial_update'] and obj.user__id == request.user.id or request.user.is_staff
