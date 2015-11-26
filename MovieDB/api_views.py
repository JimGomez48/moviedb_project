import rest_framework.views as rest_views
import rest_framework.viewsets as rest_viewsets
import rest_framework.response as rest_response
from rest_framework import authentication, permissions


class ActorsViewSet(rest_viewsets.ViewSet):
    authentication_classes = authentication.TokenAuthentication
    permission_classes = permissions.IsAdminUser

    def list(self, request):
        pass

    def create(self, actor):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, actor_id, pk=None):
        pass

    def partial_update(self, pk=None):
        pass

    def destroy(self, pk=None):
        pass
