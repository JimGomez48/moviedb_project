from django.contrib import admin

from moviedb import models

admin.site.register(models.Actor)
admin.site.register(models.Director)
admin.site.register(models.Movie)
admin.site.register(models.Review)
admin.site.register(models.MovieActor)
