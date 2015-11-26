from rest_framework import serializers
import models


class MovieSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = ('id', 'title', 'year', 'mpaa_rating', 'directors', 'cast', 'genres', 'companies')
        depth = 1

    # mpaa_rating =

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.year = validated_data.get('year', instance.year)
        instance.save()
        return instance


class MovieSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = ('id', 'title', 'year', 'mpaa_rating')
        depth = 1


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ('id', 'value')


class MpaaRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MpaaRating
        fields = ('id', 'value')


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Actor
        fields = ('id', 'last', 'first', 'sex', 'dob', 'dod')


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Director
        fields = ('id', 'last', 'first', 'dob', 'dod')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ('id', 'name')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ('id', 'time', 'user', 'movie', 'rating', 'comment')


class MovieActorSerializer(serializers.ModelSerializer):
    movie = MovieSerializerShort()
    actor = ActorSerializer()
    roles = serializers.SlugRelatedField(many=True, read_only=True,
                                         slug_field='role')

    class Meta:
        model = models.MovieActor
        fields = ('id', 'movie', 'actor', 'roles')


class MovieActorRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MovieActorRole
        fields = ('id', 'movie_actor', 'role')


class CastMemberSerializer(serializers.ModelSerializer):
    actor = ActorSerializer()
    roles = serializers.SlugRelatedField(many=True, read_only=True,
                                         slug_field='role')

    class Meta:
        model = models.MovieActor
        fields = ('actor', 'roles')


class ActorFilmEntrySerializer(serializers.Serializer):
    movie = MovieSerializerShort()
    roles = serializers.SlugRelatedField(many=True, read_only=True,
                                         slug_field='role')

    class Meta:
        model = models.MovieActor
        fields = ('movie', 'roles')
        depth = 1

# import MovieDB.models as models
# import MovieDB.serializers as serializers
# import rest_framework.renderers as renderers
