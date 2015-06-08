from django.contrib import admin
from MovieDB import models

admin.site.register(models.Actor)
admin.site.register(models.Director)
admin.site.register(models.Movie)
admin.site.register(models.Review)
admin.site.register(models.MovieActor)
admin.site.register(models.MovieDirector)
admin.site.register(models.MovieGenre)
# admin.site.register(MaxPersonID)
# admin.site.register(MaxMovieID)
