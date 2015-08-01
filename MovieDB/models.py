"""
This file constitutes the Model Layer. It is responsible for data retrieval and
persistence of model instances. Models can contain behavior logic, but should
not depend on any other model to carry out the behaviour.

The Model Layer knows about itself only.
"""

import datetime
import re
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Actor(models.Model):
    """
    :param: id - Primary key
    :param: last - Last name of the actor
    :param: first - First name of the actor
    :param: sex - Actor's sex
    :param: dob - Actor's date of birth
    :param: dod - Actor's date of death. None if still alive
    """
    class ActorManager(models.Manager):
        pass
    MALE = 'male'
    FEMALE = 'female'
    SEX_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    id = models.AutoField(primary_key=True, editable=False)
    last = models.CharField(max_length=50, blank=False, null=False, verbose_name='Last Name')
    first = models.CharField(max_length=50, blank=False, null=False, verbose_name='First Name')
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, blank=False, null=False, verbose_name='Sex')
    dob = models.DateField(verbose_name='Date of Birth')
    dod = models.DateField(null=True, default=None, verbose_name='Date of Death')
    objects = ActorManager()

    class Meta:
        ordering = ['last', 'first']

    def __unicode__(self):
        return '%s, %s (%s)' % (self.last, self.first, self.dob)

    def get_full_name(self):
        return '%s %s' % (self.first, self.last)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.dod and (self.dod < self.dob):
            raise ValidationError('Actor dod cannot be less than dob')
        # if not self.sex in self.SEX_CHOICES:
        #     raise ValidationError('invalid value for sex')
        super(Actor, self).save(force_insert, force_update, using, update_fields)


class Director(models.Model):
    """
    :param: id - Primary key
    :param: last - Last name of the director
    :param: first - First name of the director
    :param: dob - Director's date of birth
    :param: dod - Director's date of death. None if still alive
    """
    class DirectorManager(models.Manager):
        pass

    id = models.AutoField(primary_key=True, editable=False)
    last = models.CharField(max_length=20, blank=False, null=False, verbose_name='Last Name')
    first = models.CharField(max_length=20, blank=False, null=False, verbose_name='First Name')
    dob = models.DateField(blank=False, null=False, verbose_name='Date of Birth')
    dod = models.DateField(null=True, default=None, verbose_name='Date of Death')
    objects = DirectorManager()

    class Meta:
        ordering = ['last', 'first']

    def __unicode__(self):
        return '%s, %s (%s)' % (self.last, self.first, self.dob)

    def get_full_name(self):
        return '%s %s' % (self.first, self.last)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.dod and (self.dod < self.dob):
            raise ValidationError('Director dod cannot be less than dob')
        super(Director, self).save(force_insert, force_update, using, update_fields)


class Movie(models.Model):
    """
    :param: id - Primary key
    :param: title - The movie title
    :param: year - The year the movie was released
    :param: rating - MPAA rating
    :param: company - Production Company
    """
    class MovieManager(models.Manager):
        pass
    NC_17 = 'NC-17'
    R = 'R'
    PG_13 = 'PG-13'
    PG = 'PG'
    G = 'G'
    SURRENDERED = 'surrendere'
    MPAA_RATINGS = (
        (NC_17, 'NC-17'),
        (R, 'R'),
        (PG_13, 'PG-13'),
        (PG, 'PG'),
        (G, 'G'),
        (SURRENDERED, 'Not Rated'),
    )
    id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=100, blank=False, null=False, verbose_name='Movie Title', unique_for_year='year')
    year = models.IntegerField(blank=False, null=False, default=datetime.date.today().year, verbose_name='Year')
    rating = models.CharField(max_length=10, choices=MPAA_RATINGS, blank=False, verbose_name='MPAA Rating')
    company = models.CharField(max_length=50, blank=False, null=False, verbose_name='Production Company')
    objects = MovieManager()

    class Meta:
        ordering = ['title', 'year']

    def __unicode__(self):
        return '%s (%s)' % (self.title, self.year)

    def get_cleaned_title(self):
        r = re.compile(r', The$', re.IGNORECASE)
        if not re.search(r, self.title):
            return self.title
        cleaned_title = '%s %s' % ('The', str(re.sub(r, '', self.title)))
        return cleaned_title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.year < 1800 or self.year > datetime.datetime.now().year:
            raise ValidationError('Invalid year value')
        # if not self.rating in self.MPAA_RATINGS:
        #     raise ValidationError('Invalid rating value')
        super(Movie, self).save(force_insert, force_update, using, update_fields)


class Review(models.Model):
    """
    :param: id - Primary key
    :param: time - The datetime at which the review was made
    :param: user_name - User name of the person who wrote the review
    :param: mid - Movie foreign key to which this review refers
    :param: rating - Rating (1-5 stars)
    :param: comment - User's review comments
    """
    MIN = 1
    MAX = 5
    RATING_RANGE = (
        (1, '1-star'),
        (2, '2-star'),
        (3, '3-star'),
        (4, '4-star'),
        (5, '5-star'),
    )
    id = models.AutoField(primary_key=True, editable=False)
    time = models.DateTimeField(auto_now=True, editable=False, verbose_name='Time')
    user_name = models.CharField(max_length=20, blank=False, null=False, verbose_name='User Name')
    mid = models.ForeignKey(Movie, db_column='mid', on_delete=models.CASCADE, verbose_name='Movie')
    rating = models.IntegerField(choices=RATING_RANGE, blank=False, null=False, default=5, verbose_name='User Rating')
    comment = models.TextField(max_length=2000, blank=True, default='')

    class Meta:
        ordering = ['-time']

    def __unicode__(self):
        return 'mid:%s user:%s time:%s rating:%s' % (self.mid, self.user_name, self.time, self.rating)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Review.rating cannot be outside the range [1,5]')
        super(Review, self).save(force_insert, force_update, using, update_fields)


class MovieActor(models.Model):
    """
    :param: id - Primary key
    :param: mid - Movie foreign key
    :param: aid - Actor foreign key
    :param: role - Actor's role in this movie
    """
    id = models.AutoField(primary_key=True, editable=False)
    mid = models.ForeignKey(Movie, db_column='mid', on_delete=models.CASCADE, verbose_name='Movie')
    aid = models.ForeignKey(Actor, db_column='aid', on_delete=models.CASCADE, verbose_name='Actor')
    role = models.CharField(max_length=50, blank=False, null=False, verbose_name='Role')

    def __unicode__(self):
        return 'id:%s mid:%s aid:%s' % (self.id, self.mid, self.aid)


class MovieDirector(models.Model):
    """
    :param: id - Primary key
    :param: mid - Movie foreign key
    :param: did - Director foreign key
    """
    id = models.AutoField(primary_key=True, editable=False)
    mid = models.ForeignKey(Movie, db_column='mid', on_delete=models.CASCADE, verbose_name='Movie')
    did = models.ForeignKey(Director, db_column='did', on_delete=models.CASCADE, verbose_name='Director')

    def __unicode__(self):
        return 'id:%s mid:%s aid:%s' % (self.id, self.mid, self.did)


class MovieGenre(models.Model):
    """
    :param: id - Primary key
    :param: mid - Movie foreign key
    :param: genre - A genre of this movie
    """
    ACTION = 'Action'
    ADULT = 'Adult'
    ADV ='Adventure'
    ANIM ='Animation'
    CRIME ='Crime'
    COMEDY = 'Comedy'
    DOC ='Documentary'
    DRAMA ='Drama'
    FAM ='Family'
    FANT ='Fantasy'
    HORROR ='Horror'
    MUS = 'Musical'
    MYST ='Mystery'
    ROM ='Romance'
    SCI_FI ='Sci-Fi'
    SHORT ='Short'
    THRILL = 'Thriller'
    WAR = 'War'
    WEST ='Western'
    GENRE_CHOICES = (
        (ACTION, 'Action'),
        (ADULT, 'Adult'),
        (ADV, 'Adventure'),
        (ANIM, 'Animation'),
        (CRIME, 'Crime'),
        (COMEDY, 'Comedy'),
        (DOC, 'Documentary'),
        (DRAMA, 'Drama'),
        (FAM, 'Family'),
        (FANT, 'Fantasy'),
        (HORROR, 'Horror'),
        (MUS, 'Musical'),
        (MYST, 'Mystery'),
        (ROM, 'Romance'),
        (SCI_FI, 'Sci-Fi'),
        (SHORT, 'Short'),
        (THRILL, 'Thriller'),
        (WAR, 'War'),
        (WEST, 'Western'),
    )
    id = models.AutoField(primary_key=True, editable=False)
    mid = models.ForeignKey(Movie, db_column='mid', on_delete=models.CASCADE, verbose_name='Movie')
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, blank=False, null=False, default='Drama', verbose_name='Genre')

    def __unicode__(self):
        return 'id:%s mid:%s genre:%s' % (self.id, self.mid, self.genre)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # if not self.genre in self.GENRE_CHOICES:
        #     raise ValidationError('Invalid genre value')
        super(MovieGenre, self).save(force_insert, force_update, using, update_fields)
