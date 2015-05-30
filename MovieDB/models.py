import datetime
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import managers

# ############################
# # standalone model entities
# ############################
class Actor(models.Model):
    SEX_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )
    id = models.IntegerField(primary_key=True)
    last = models.CharField(max_length=20)
    first = models.CharField(max_length=20)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)
    dob = models.DateField()
    dod = models.DateField(null=True, default=None)

    def __init__(self):
        super(Actor, self).__init__()
        self.objects = managers.ActorManager()

    def get_full_name(self):
        full_name = '%s %s' % (self.first, self.last)
        return full_name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.dod and self.dod < self.dob:
            raise ValidationError('dod cannot be less than dod')
        if not self.sex in self.SEX_CHOICES:
            raise ValidationError('invalid value for sex')
        super(Actor, self).save(force_insert, force_update, using, update_fields)


class Director(models.Model):
    id = models.IntegerField(primary_key=True)
    last = models.CharField(max_length=20)
    first = models.CharField(max_length=20)
    dob = models.DateField()
    dod = models.DateField(null=True, default=None)

    def get_full_name(self):
        full_name = '%s %s' % (self.first, self.last)
        return full_name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.dod and self.dod < self.dob:
            raise ValidationError('Director.dod cannot be less than Director.dob')
        super(Director, self).save(force_insert, force_update, using, update_fields)


class Movie(models.Model):
    MPAA_RATINGS = (
        ('NC-17', 'NC-17'),
        ('R', 'R'),
        ('PG-13', 'PG-13'),
        ('PG', 'PG'),
        ('G', 'G'),
        ('surrendere', 'surrendere'),
    )
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    year = models.IntegerField(blank=True, default='')
    rating = models.CharField(max_length=10, choices=MPAA_RATINGS)
    company = models.CharField(max_length=50)

    def __init__(self):
        super(Movie, self).__init__()
        self.objects = managers.MovieManager()

def save(self, force_insert=False, force_update=False, using=None,
         update_fields=None):
    if self.year < 1800 or self.year > datetime.datetime.now().year:
        raise ValidationError('Invalid year value')
    if not self.rating in self.MPAA_RATINGS:
        raise ValidationError('Invalid rating value')
    super(Movie, self).save(force_insert, force_update, using, update_fields)


class Review(models.Model):
    RATING_RANGE = (
        (1, '1-star'),
        (2, '2-star'),
        (3, '3-star'),
        (4, '4-star'),
        (5, '5-star'),
    )
    id = models.AutoField(primary_key=True, editable=False)
    time = models.DateTimeField(auto_now=True, editable=False)
    name = models.CharField(max_length=20)
    mid = models.ForeignKey(Movie, db_column='mid')
    rating = models.IntegerField(choices=RATING_RANGE)
    comment = models.CharField(max_length=500, blank=True, default='')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Review.rating cannot be outside the range [1,5]')
        super(Review, self).save(force_insert, force_update, using, update_fields)


##########################
# model relation entities
##########################
#
class MovieActor(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    mid = models.ForeignKey(Movie, db_column='mid')
    aid = models.ForeignKey(Actor, db_column='aid')
    role = models.CharField(max_length=50)


#
class MovieDirector(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    mid = models.ForeignKey(Movie, db_column='mid')
    did = models.ForeignKey(Director, db_column='did')


#
class MovieGenre(models.Model):
    GENRE_CHOICES = (
        ('Action', 'Action'),
        ('Adult', 'Adult'),
        ('Adventure', 'Adventure'),
        ('Animation', 'Animation'),
        ('Crime', 'Crime'),
        ('Comedy', 'Comedy'),
        ('Documentary', 'Documentary'),
        ('Drama', 'Drama'),
        ('Family', 'Family'),
        ('Fantasy', 'Fantasy'),
        ('Horror', 'Horror'),
        ('Musical', 'Musical'),
        ('Mystery', 'Mystery'),
        ('Romance', 'Romance'),
        ('Sci-Fi', 'Sci-Fi'),
        ('Short', 'Short'),
        ('Thriller', 'Thriller'),
        ('War', 'War'),
        ('Western', 'Western'),
    )
    id = models.AutoField(primary_key=True, editable=False)
    mid = models.ForeignKey(Movie, db_column='mid')
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.genre in self.GENRE_CHOICES:
            raise ValidationError('Invalid genre value')
        super(MovieGenre, self).save(force_insert, force_update, using, update_fields)


class MaxPersonID(models.Model):
    id = models.IntegerField(primary_key=True)


class MaxMovieID(models.Model):
    id = models.IntegerField(primary_key=True)
