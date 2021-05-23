from rest_framework import permissions


class SentencePermission(permissions.BasePermission):

    anonymous_actions = ()
    authorized_actions = ('create', 'update')

    @staticmethod
    def _is_authenticated(request):
        return request.user and request.user.is_authenticated

    @classmethod
    def _is_admin(cls, request):
        return cls._is_authenticated(request) and request.user.is_superuser

    def has_permission(self, request, view):
        return any((self._is_admin(request),
                    view.action in self.anonymous_actions and self._is_authenticated(request),
                    view.action in self.authorized_actions and self._is_authenticated(request)))


class MistakePermission(permissions.BasePermission):

    anonymous_actions = ()
    authorized_actions = ('update')

    @staticmethod
    def _is_authenticated(request):
        return request.user and request.user.is_authenticated

    @classmethod
    def _is_admin(cls, request):
        return cls._is_authenticated(request) and request.user.is_superuser

    def has_permission(self, request, view):
        return any((self._is_admin(request),
                    view.action in self.anonymous_actions and self._is_authenticated(request),
                    view.action in self.authorized_actions and self._is_authenticated(request)))
