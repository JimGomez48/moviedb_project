from rest_framework import serializers
import models


class MovieSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = ('id', 'title', 'year', 'mpaa_rating')
        depth = 1

    title = serializers.CharField(source='cleaned_title')
    mpaa_rating = serializers.SlugRelatedField(read_only=True, slug_field='value')


class ActorFilmEntrySerializer(serializers.Serializer):
    class Meta:
        model = models.MovieActor
        fields = ('movie', 'roles')
        depth = 1

    movie = MovieSerializerShort()
    roles = serializers.SlugRelatedField(many=True, read_only=True, slug_field='role')


class DirectorFilmEntrySerializer(serializers.Serializer):
    class Meta:
        model = models.MovieDirector
        fields = ('movie')
        depth = 1

    movie = MovieSerializerShort()


class ActorSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = models.Actor
        fields = ('id', 'last', 'first', 'sex', 'dob', 'dod')


class ActorSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = models.Actor
        fields = ('id', 'last', 'first', 'sex', 'dob', 'dod', 'filmography')

    filmography = ActorFilmEntrySerializer(many=True, source='movieactor_set')


class CastMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MovieActor
        fields = ('actor', 'roles')

    actor = ActorSerializerShort()
    roles = serializers.SlugRelatedField(many=True, read_only=True, slug_field='role')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ('id', 'time', 'user', 'movie', 'rating', 'comment')


class MovieSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = ('id', 'title', 'year', 'mpaa_rating', 'directors', 'cast', 'genres', 'companies', 'reviews')
        depth = 2

    title = serializers.CharField(source='cleaned_title')
    mpaa_rating = serializers.SlugRelatedField(read_only=True, slug_field='value')
    cast = CastMemberSerializer(many=True, source='movieactor_set')
    reviews = ReviewSerializer(many=True, source='review_set')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.year = validated_data.get('year', instance.year)
        instance.save()
        return instance


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ('id', 'value')


class MpaaRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MpaaRating
        fields = ('id', 'value')


class DirectorSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = models.Director
        fields = ('id', 'last', 'first', 'dob', 'dod')


class DirectorSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = models.Director
        fields = ('id', 'last', 'first', 'dob', 'dod', 'filmography')

    filmography = DirectorFilmEntrySerializer(many=True, source='moviedirector_set')


class MovieDirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MovieDirector

class CompanySerializerShort(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ('id', 'name')


class CompanySerializerFull(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ('id', 'name', 'movies')

    movies = MovieSerializerShort(many=True, source='movie_set')


class MovieActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MovieActor
        fields = ('id', 'movie', 'actor', 'roles')

    movie = MovieSerializerShort()
    actor = ActorSerializerFull()
    roles = serializers.SlugRelatedField(many=True, read_only=True, slug_field='role')


class MovieActorRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MovieActorRole
        fields = ('id', 'movie_actor', 'role')
