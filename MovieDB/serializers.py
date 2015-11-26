from rest_framework import serializers
import models

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = ('id', 'title', 'year', 'mpaa_rating', 'directors', 'cast', 'genres', 'companies')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.year = validated_data.get('year', instance.year)
        instance.save()
        return instance