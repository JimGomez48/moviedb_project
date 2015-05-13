import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# ############################
# # standalone model entities
# ############################
class Actor(models.Model):
    SEX_CHOICES = (
        ('male', 'male'),
        ('male', 'female'),
    )
    id = models.IntegerField(primary_key=True, default=-1)
    last = models.CharField(max_length=20, null=False, default='')
    first = models.CharField(max_length=20, null=False, default='')
    sex = models.CharField(max_length=6, null=False, default='', choices=SEX_CHOICES)
    dob = models.DateField(null=False, default=datetime.date(1800, 1, 1), blank=True)
    dod = models.DateField(null=True, blank=True)


class Director(models.Model):
    id = models.IntegerField(primary_key=True, default=-1)
    last = models.CharField(max_length=20, null=False, default='')
    first = models.CharField(max_length=20, null=False, default='')
    dob = models.DateField(null=False, default=datetime.date(1800, 1, 1), blank=True)
    dod = models.DateField(null=True, default=None)


class Movie(models.Model):
    MPAA_RATINGS = (
        ('NC-17', 'NC-17'),
        ('R', 'R'),
        ('PG-13', 'PG-13'),
        ('PG', 'PG'),
        ('G', 'G'),
        ('surrendere', 'surrendere'),
    )
    id = models.IntegerField(primary_key=True, default=-1)
    title = models.CharField(max_length=100, null=False, default='')
    year = models.IntegerField(null=True)
    rating = models.CharField(max_length=10, null=False, default='', choices=MPAA_RATINGS)
    company = models.CharField(max_length=50, null=True)


class Review(models.Model):
    RATING_RANGE = (
        (1, '1-star'),
        (2, '2-star'),
        (3, '3-star'),
        (4, '4-star'),
        (5, '5-star'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False, default='')
    time = models.DateTimeField(null=False, default=datetime.datetime(1800, 1, 1), blank=True)
    mid = models.IntegerField(null=False, default=-1)
    rating = models.IntegerField(null=False, default=-1, choices=RATING_RANGE)
    comment = models.CharField(max_length=500, null=True)

##########################
# model relation entities
##########################
class MovieActor(models.Model):
    pass

class MovieDirector(models.Model):
    pass

class MovieGenre(models.Model):
    pass

class MaxPersonID(models.Model):
    pass

class MaxMovieID(models.Model):
    pass