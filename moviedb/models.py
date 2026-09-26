import re
from datetime import UTC, datetime
from typing import ClassVar

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg


def current_year():
    return datetime.now(UTC).year


class Actor(models.Model):
    MALE = "male"
    FEMALE = "female"
    SEX_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
    )

    last = models.CharField(
        max_length=50, blank=False, null=False, verbose_name="Last Name"
    )
    first = models.CharField(
        max_length=50, blank=False, null=False, verbose_name="First Name"
    )
    sex = models.CharField(
        max_length=6, choices=SEX_CHOICES, blank=False, null=False, verbose_name="Sex"
    )
    dob = models.DateField(verbose_name="Date of Birth")
    dod = models.DateField(null=True, default=None, verbose_name="Date of Death")

    class Meta:
        db_table = "actors"
        ordering: ClassVar[list[str]] = ["last", "first"]

    def __str__(self):
        return f"[{self.pk}] {self.last}, {self.first} ({self.dob})"

    def get_full_name(self):
        return f"{self.first} {self.last}"

    def save(self, *args, **kwargs):
        if self.dod and (self.dod < self.dob):
            raise ValidationError("Actor dod cannot be less than dob")
        # if not self.sex in self.SEX_CHOICES:
        #     raise ValidationError('invalid value for sex')
        super().save(*args, **kwargs)


class Director(models.Model):
    last = models.CharField(
        max_length=20, blank=False, null=False, verbose_name="Last Name"
    )
    first = models.CharField(
        max_length=20, blank=False, null=False, verbose_name="First Name"
    )
    dob = models.DateField(blank=False, null=False, verbose_name="Date of Birth")
    dod = models.DateField(null=True, default=None, verbose_name="Date of Death")

    class Meta:
        db_table = "directors"
        ordering: ClassVar[list[str]] = ["last", "first"]

    def __str__(self):
        return f"[{self.pk}] {self.last}, {self.first} ({self.dob})"

    def get_full_name(self):
        return f"{self.first} {self.last}"

    def save(self, *args, **kwargs):
        if self.dod and (self.dod < self.dob):
            raise ValidationError("Director dod cannot be less than dob")
        super().save(*args, **kwargs)


class MpaaRating(models.Model):
    NC_17 = "NC-17"
    R = "R"
    PG_13 = "PG-13"
    PG = "PG"
    G = "G"
    SURRENDERED = "surrendered"
    RATINGS = (
        (NC_17, "NC-17"),
        (R, "R"),
        (PG_13, "PG-13"),
        (PG, "PG"),
        (G, "G"),
        (SURRENDERED, "Not Rated"),
    )

    value = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        choices=RATINGS,
        verbose_name="Mpaa Rating Value",
    )

    class Meta:
        db_table = "mpaa_ratings"

    def __str__(self):
        return f"[{self.pk}] {self.value}"


class Genre(models.Model):
    ACTION = "Action"
    ADULT = "Adult"
    ADV = "Adventure"
    ANIM = "Animation"
    CRIME = "Crime"
    COMEDY = "Comedy"
    DOC = "Documentary"
    DRAMA = "Drama"
    FAM = "Family"
    FANT = "Fantasy"
    HORROR = "Horror"
    MUS = "Musical"
    MYST = "Mystery"
    ROM = "Romance"
    SCI_FI = "Sci-Fi"
    SHORT = "Short"
    THRILL = "Thriller"
    WAR = "War"
    WEST = "Western"
    GENRES = (
        (ACTION, "Action"),
        (ADULT, "Adult"),
        (ADV, "Adventure"),
        (ANIM, "Animation"),
        (CRIME, "Crime"),
        (COMEDY, "Comedy"),
        (DOC, "Documentary"),
        (DRAMA, "Drama"),
        (FAM, "Family"),
        (FANT, "Fantasy"),
        (HORROR, "Horror"),
        (MUS, "Musical"),
        (MYST, "Mystery"),
        (ROM, "Romance"),
        (SCI_FI, "Sci-Fi"),
        (SHORT, "Short"),
        (THRILL, "Thriller"),
        (WAR, "War"),
        (WEST, "Western"),
    )
    value = models.CharField(
        max_length=20,
        choices=GENRES,
        blank=False,
        null=False,
        default="Drama",
        verbose_name="Genre Value",
    )

    class Meta:
        db_table = "genres"

    def __str__(self):
        return f"[{self.pk}] {self.value}"


class Company(models.Model):
    name = models.CharField(
        max_length=50, blank=False, null=False, verbose_name="Company Name"
    )

    class Meta:
        db_table = "companies"

    def __str__(self):
        return f"[{self.pk}]: {self.name}"


class Movie(models.Model):
    title = models.CharField(
        max_length=100, blank=False, null=False, verbose_name="Movie Title"
    )
    year = models.IntegerField(
        blank=False, null=False, default=current_year, verbose_name="Year"
    )
    mpaa_rating = models.ForeignKey(
        MpaaRating, on_delete=models.PROTECT, verbose_name="Mpaa Rating"
    )
    cast = models.ManyToManyField(Actor, through="MovieActor")
    directors = models.ManyToManyField(Director, through="MovieDirector")
    genres = models.ManyToManyField(Genre, through="MovieGenre")
    companies = models.ManyToManyField(Company, through="MovieCompany")

    class Meta:
        db_table = "movies"
        ordering: ClassVar[list[str]] = ["title", "year"]
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(
                fields=["title", "year"], name="unique_movie_title_year"
            ),
        ]

    def __str__(self):
        return f"[{self.pk}] {self.title} ({self.year})"

    def get_cleaned_title(self):
        r = re.compile(r", The$", re.IGNORECASE)
        if not re.search(r, self.title):
            return self.title
        cleaned_title = f"The {re.sub(r, '', self.title)}"
        return cleaned_title

    def avg_user_rating(self):
        return self.review_set.aggregate(Avg("rating"))["rating__avg"]

    def save(self, *args, **kwargs):
        if self.year < 1800 or self.year > datetime.now(UTC).year:
            raise ValidationError("Invalid year value")
        # if not self.rating in self.MPAA_RATINGS:
        #     raise ValidationError('Invalid rating value')
        super().save(*args, **kwargs)


class Review(models.Model):
    RATING_CHOICES = (
        (1, "1-star"),
        (2, "2-star"),
        (3, "3-star"),
        (4, "4-star"),
        (5, "5-star"),
    )

    time = models.DateTimeField(auto_now=True, editable=False, verbose_name="Time")
    user_name = models.CharField(
        max_length=20, blank=False, null=False, verbose_name="User Name"
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Movie")
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        blank=False,
        null=False,
        default=5,
        verbose_name="User Rating",
    )
    comment = models.TextField(max_length=2000, blank=True, default="")

    class Meta:
        db_table = "reviews"
        ordering: ClassVar[list[str]] = ["-time"]

    def __str__(self):
        return f"[{self.pk}] movie:{self.movie.pk} user:{self.user_name} time:{self.time} rating:{self.rating}"

    def save(self, *args, **kwargs):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError("Review.rating cannot be outside the range [1,5]")
        super().save(*args, **kwargs)


class MovieCompany(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Movie")
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, verbose_name="Company"
    )

    class Meta:
        db_table = "movie_companies"

    def __str__(self):
        return f"[{self.pk}] movie={self.movie.pk} company={self.company.pk}"


class MovieActor(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Movie")
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, verbose_name="Actor")

    class Meta:
        db_table = "movie_actors"

    def __str__(self):
        return f"[{self.pk}] movie={self.movie.pk} actor={self.actor.pk}"

    def roles(self):
        return self.movieactorrole_set.all().values_list("role", flat=True)


class MovieActorRole(models.Model):
    movie_actor = models.ForeignKey(MovieActor, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, blank=False, null=False, verbose_name="Role")

    class Meta:
        db_table = "movie_actor_roles"

    def __str__(self):
        return f"[{self.pk}] movie={self.movie_actor.pk} role={self.role}"


class MovieDirector(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Movie")
    director = models.ForeignKey(
        Director, on_delete=models.CASCADE, verbose_name="Director"
    )

    class Meta:
        db_table = "movie_directors"

    def __str__(self):
        return f"[{self.pk}] movie={self.movie.pk} director={self.director.pk}"


class MovieGenre(models.Model):
    ACTION = "Action"
    ADULT = "Adult"
    ADV = "Adventure"
    ANIM = "Animation"
    CRIME = "Crime"
    COMEDY = "Comedy"
    DOC = "Documentary"
    DRAMA = "Drama"
    FAM = "Family"
    FANT = "Fantasy"
    HORROR = "Horror"
    MUS = "Musical"
    MYST = "Mystery"
    ROM = "Romance"
    SCI_FI = "Sci-Fi"
    SHORT = "Short"
    THRILL = "Thriller"
    WAR = "War"
    WEST = "Western"
    GENRE_CHOICES = (
        (ACTION, "Action"),
        (ADULT, "Adult"),
        (ADV, "Adventure"),
        (ANIM, "Animation"),
        (CRIME, "Crime"),
        (COMEDY, "Comedy"),
        (DOC, "Documentary"),
        (DRAMA, "Drama"),
        (FAM, "Family"),
        (FANT, "Fantasy"),
        (HORROR, "Horror"),
        (MUS, "Musical"),
        (MYST, "Mystery"),
        (ROM, "Romance"),
        (SCI_FI, "Sci-Fi"),
        (SHORT, "Short"),
        (THRILL, "Thriller"),
        (WAR, "War"),
        (WEST, "Western"),
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Movie")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name="Movie")

    class Meta:
        db_table = "movie_genres"

    def __str__(self):
        return f"[{self.pk}] movie={self.movie.pk} genre={self.genre.pk}"

    def save(self, *args, **kwargs):
        # if not self.genre in self.GENRE_CHOICES:
        #     raise ValidationError('Invalid genre value')
        super().save(*args, **kwargs)
