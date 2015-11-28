import rest_framework.views as rest_views
import rest_framework.viewsets as viewsets
import rest_framework.response as response
from rest_framework import authentication, permissions

import models
import serializers

# class ActorsViewSet(viewsets.ViewSet):
#     authentication_classes = authentication.TokenAuthentication
#     permission_classes = permissions.IsAdminUser
#
#     def list(self, request):
#         queryset = Actor.objects.all()
#         serializer = ActorSerializer(queryset, many=True)
#         return response.Response(serializer.data)
#
#     def create(self, actor):
#         pass
#
#     def retrieve(self, request, pk=None):
#         pass
#
#     def update(self, actor_id, pk=None):
#         pass
#
#     def partial_update(self, pk=None):
#         pass
#
#     def destroy(self, pk=None):
#         pass

class MoviesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MovieSerializerShort
    queryset = models.Movie.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.MovieSerializerFull(instance)
        return response.Response(serializer.data)


class ActorsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ActorSerializerShort
    queryset = models.Actor.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.ActorSerializerFull(instance)
        return response.Response(serializer.data)


class DirectorsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DirectorSerializerShort
    queryset = models.Director.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.DirectorSerializerFull(instance)
        return response.Response(serializer.data)


class CompaniesViewSet(viewsets.ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializerShort

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.CompanySerializerFull(instance)
        return response.Response(serializer.data)


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

# import MovieDB.models as models
# import MovieDB.serializers as serializers
# import rest_framework.renderers as renderers
