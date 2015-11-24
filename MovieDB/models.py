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
from django.db.models import Avg


def validate_dob_dod(dob):
    pass

class Actor(models.Model):
    """
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

    last = models.CharField(max_length=50, blank=False, null=False, verbose_name='Last Name')
    first = models.CharField(max_length=50, blank=False, null=False, verbose_name='First Name')
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, blank=False, null=False, verbose_name='Sex')
    dob = models.DateField(verbose_name='Date of Birth')
    dod = models.DateField(null=True, default=None, verbose_name='Date of Death')
    objects = ActorManager()

    class Meta:
        db_table = 'actors'
        ordering = ['last', 'first']

    def __unicode__(self):
        return '[%s] %s, %s (%s)' % (self.id, self.last, self.first, self.dob)

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
    :param: last - Last name of the director
    :param: first - First name of the director
    :param: dob - Director's date of birth
    :param: dod - Director's date of death. None if still alive
    """
    class DirectorManager(models.Manager):
        pass

    last = models.CharField(max_length=20, blank=False, null=False, verbose_name='Last Name')
    first = models.CharField(max_length=20, blank=False, null=False, verbose_name='First Name')
    dob = models.DateField(blank=False, null=False, verbose_name='Date of Birth')
    dod = models.DateField(null=True, default=None, verbose_name='Date of Death')
    objects = DirectorManager()

    class Meta:
        db_table = 'directors'
        ordering = ['last', 'first']

    def __unicode__(self):
        return '[%s] %s, %s (%s)' % (self.id, self.last, self.first, self.dob)

    def get_full_name(self):
        return '%s %s' % (self.first, self.last)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.dod and (self.dod < self.dob):
            raise ValidationError('Director dod cannot be less than dob')
        super(Director, self).save(force_insert, force_update, using, update_fields)


class MpaaRating(models.Model):
    NC_17       = 'NC-17'
    R           = 'R'
    PG_13       = 'PG-13'
    PG          = 'PG'
    G           = 'G'
    SURRENDERED = 'surrendered'
    RATINGS = (
        (NC_17, 'NC-17'),
        (R, 'R'),
        (PG_13, 'PG-13'),
        (PG, 'PG'),
        (G, 'G'),
        (SURRENDERED, 'Not Rated'),
    )

    value = models.CharField(max_length=20, blank=False, null=False, choices=RATINGS, verbose_name='Mpaa Rating Value')

    class Meta:
        db_table = 'mpaa_ratings'

    def __unicode__(self):
        return '[%s] %s' % (self.id, self.value)


class Genre(models.Model):
    ACTION  = 'Action'
    ADULT   = 'Adult'
    ADV     = 'Adventure'
    ANIM    = 'Animation'
    CRIME   = 'Crime'
    COMEDY  = 'Comedy'
    DOC     = 'Documentary'
    DRAMA   = 'Drama'
    FAM     = 'Family'
    FANT    = 'Fantasy'
    HORROR  = 'Horror'
    MUS     = 'Musical'
    MYST    = 'Mystery'
    ROM     = 'Romance'
    SCI_FI  = 'Sci-Fi'
    SHORT   = 'Short'
    THRILL  = 'Thriller'
    WAR     = 'War'
    WEST    ='Western'
    GENRES = (
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
    value = models.CharField(max_length=20, choices=GENRES, blank=False, null=False, default='Drama', verbose_name='Genre Value')

    class Meta:
        db_table = 'genres'

    def __unicode__(self):
        return '[%s] %s' % (self.id, self.value)


class Company(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, verbose_name='Company Name')

    class Meta:
        db_table = 'companies'

    def __unicode__(self):
        return '[%s]: %s' % (self.id, self.name)


class Movie(models.Model):
    """
    :param: title       - The movie title
    :param: year        - The year the movie was released
    :param: mpaa_rating - MPAA rating
    :param: company     - Production Company
    """
    class MovieManager(models.Manager):
        pass

    title = models.CharField(max_length=100, blank=False, null=False, verbose_name='Movie Title', unique_for_year='year')
    year = models.IntegerField(blank=False, null=False, default=datetime.date.today().year, verbose_name='Year')
    mpaa_rating = models.ForeignKey(MpaaRating, on_delete=models.PROTECT, verbose_name='Mpaa Rating')
    cast = models.ManyToManyField(Actor, through='MovieActor')
    directors = models.ManyToManyField(Director, through='MovieDirector')
    genres = models.ManyToManyField(Genre, through='MovieGenre')
    companies = models.ManyToManyField(Company, through='MovieCompany')
    objects = MovieManager()

    class Meta:
        db_table = 'movies'
        ordering = ['title', 'year']

    def __unicode__(self):
        return '[%s] %s (%s)' % (self.id, self.title, self.year)

    def get_cleaned_title(self):
        r = re.compile(r', The$', re.IGNORECASE)
        if not re.search(r, self.title):
            return self.title
        cleaned_title = '%s %s' % ('The', str(re.sub(r, '', self.title)))
        return cleaned_title

    def avg_user_rating(self):
        return self.review_set.aggregate(Avg('rating'))['rating__avg']

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.year < 1800 or self.year > datetime.datetime.now().year:
            raise ValidationError('Invalid year value')
        # if not self.rating in self.MPAA_RATINGS:
        #     raise ValidationError('Invalid rating value')
        super(Movie, self).save(force_insert, force_update, using, update_fields)


class Review(models.Model):
    """
    :param: time - The datetime at which the review was made
    :param: user_name - User name of the person who wrote the review
    :param: movie - Movie foreign key to which this review refers
    :param: rating - Rating (1-5 stars)
    :param: comment - User's review comments
    """
    RATING_CHOICES = (
        (1, '1-star'),
        (2, '2-star'),
        (3, '3-star'),
        (4, '4-star'),
        (5, '5-star'),
    )

    time = models.DateTimeField(auto_now=True, editable=False, verbose_name='Time')
    user_name = models.CharField(max_length=20, blank=False, null=False, verbose_name='User Name')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Movie')
    rating = models.IntegerField(choices=RATING_CHOICES, blank=False, null=False, default=5, verbose_name='User Rating')
    comment = models.TextField(max_length=2000, blank=True, default='')

    class Meta:
        db_table = 'reviews'
        ordering = ['-time']

    def __unicode__(self):
        return '[%s] movie:%s user:%s time:%s rating:%s' % (self.id, self.movie.id, self.user_name, self.time, self.rating)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Review.rating cannot be outside the range [1,5]')
        super(Review, self).save(force_insert, force_update, using, update_fields)


class MovieCompany(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Movie')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Company')

    class Meta:
        db_table = 'movie_companies'

    def __unicode__(self):
        return '[%s] movie=%s company=%s' % (self.id, self.movie.id, self.company.id)


class MovieActor(models.Model):
    """
    :param: movie - Movie foreign key
    :param: actor - Actor foreign key
    """
    class MovieActorManager(models.Manager):
        pass

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Movie')
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, verbose_name='Actor')
    objects = MovieActorManager

    class Meta:
        db_table = 'movie_actors'

    def __unicode__(self):
        return '[%s] movie=%s actor=%s' % (self.id, self.movie.id, self.actor.id)

    def roles(self):
        return self.movieactorrole_set.all().values_list('role', flat=True)


class MovieActorRole(models.Model):
    movie_actor = models.ForeignKey(MovieActor, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, blank=False, null=False, verbose_name='Role')

    class Meta:
        db_table = 'movie_actor_roles'

    def __unicode__(self):
        return '[%s] movie=%s role=%s' % (self.id, self.movie_actor.id, self.role)


class MovieDirector(models.Model):
    """
    :param: movie - Movie foreign key
    :param: director - Director foreign key
    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Movie')
    director = models.ForeignKey(Director, on_delete=models.CASCADE, verbose_name='Director')

    class Meta:
        db_table = 'movie_directors'

    def __unicode__(self):
        return '[%s] movie=%s director=%s' % (self.id, self.movie.id, self.director.id)


class MovieGenre(models.Model):
    """
    :param: mid - Movie foreign key
    :param: genre - A genre of this movie
    """
    ACTION  = 'Action'
    ADULT   = 'Adult'
    ADV     = 'Adventure'
    ANIM    = 'Animation'
    CRIME   = 'Crime'
    COMEDY  = 'Comedy'
    DOC     = 'Documentary'
    DRAMA   = 'Drama'
    FAM     = 'Family'
    FANT    = 'Fantasy'
    HORROR  = 'Horror'
    MUS     = 'Musical'
    MYST    = 'Mystery'
    ROM     = 'Romance'
    SCI_FI  = 'Sci-Fi'
    SHORT   = 'Short'
    THRILL  = 'Thriller'
    WAR     = 'War'
    WEST    ='Western'
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
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Movie')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name='Movie')

    class Meta:
        db_table = 'movie_genres'

    def __unicode__(self):
        return '[%s] movie:%s genre:%s' % (self.id, self.movie.id, self.genre.id)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # if not self.genre in self.GENRE_CHOICES:
        #     raise ValidationError('Invalid genre value')
        super(MovieGenre, self).save(force_insert, force_update, using, update_fields)
