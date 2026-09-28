import re
from datetime import UTC, datetime
from typing import ClassVar

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg

MIN_YEAR = 1800


def current_year():
    return datetime.now(UTC).year


def validate_year(value):
    if not MIN_YEAR <= value <= current_year():
        raise ValidationError(
            f"Year must be between {MIN_YEAR} and {current_year()}.", code="invalid"
        )


class Actor(models.Model):
    class Sex(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    last = models.CharField(max_length=50, verbose_name="Last Name")
    first = models.CharField(max_length=50, verbose_name="First Name")
    sex = models.CharField(max_length=6, choices=Sex, verbose_name="Sex")
    dob = models.DateField(verbose_name="Date of Birth")
    dod = models.DateField(
        null=True, blank=True, default=None, verbose_name="Date of Death"
    )

    class Meta:
        ordering: ClassVar[list[str]] = ["last", "first"]
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.CheckConstraint(
                condition=models.Q(dod__isnull=True)
                | models.Q(dod__gte=models.F("dob")),
                name="actor_dod_gte_dob",
                violation_error_message="Date of death cannot be before date of birth.",
            ),
        ]

    def __str__(self):
        return f"[{self.pk}] {self.last}, {self.first} ({self.dob})"

    def get_full_name(self):
        return f"{self.first} {self.last}"

    def clean(self):
        if self.dod and self.dob and self.dod < self.dob:
            raise ValidationError(
                {"dod": "Date of death cannot be before date of birth."}
            )


class Director(models.Model):
    last = models.CharField(max_length=20, verbose_name="Last Name")
    first = models.CharField(max_length=20, verbose_name="First Name")
    dob = models.DateField(verbose_name="Date of Birth")
    dod = models.DateField(
        null=True, blank=True, default=None, verbose_name="Date of Death"
    )

    class Meta:
        ordering: ClassVar[list[str]] = ["last", "first"]
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.CheckConstraint(
                condition=models.Q(dod__isnull=True)
                | models.Q(dod__gte=models.F("dob")),
                name="director_dod_gte_dob",
                violation_error_message="Date of death cannot be before date of birth.",
            ),
        ]

    def __str__(self):
        return f"[{self.pk}] {self.last}, {self.first} ({self.dob})"

    def get_full_name(self):
        return f"{self.first} {self.last}"

    def clean(self):
        if self.dod and self.dob and self.dod < self.dob:
            raise ValidationError(
                {"dod": "Date of death cannot be before date of birth."}
            )


class MpaaRating(models.Model):
    class MpaaRatings(models.TextChoices):
        NC_17 = "NC-17", "NC-17"
        R = "R", "R"
        PG_13 = "PG-13", "PG-13"
        PG = "PG", "PG"
        G = "G", "G"
        SURRENDERED = "surrendered", "Not Rated"

    value = models.CharField(
        max_length=20,
        choices=MpaaRatings,
        verbose_name="Mpaa Rating Value",
    )

    def __str__(self):
        return f"[{self.pk}] {self.value}"


class Genre(models.Model):
    class Genres(models.TextChoices):
        ACTION = "Action"
        ADULT = "Adult"
        ADVENTURE = "Adventure"
        ANIMATION = "Animation"
        CRIME = "Crime"
        COMEDY = "Comedy"
        DOCUMENTARY = "Documentary"
        DRAMA = "Drama"
        FAMILY = "Family"
        FANTASY = "Fantasy"
        HORROR = "Horror"
        MUSICAL = "Musical"
        MYSTERY = "Mystery"
        ROMANCE = "Romance"
        SCI_FI = "Sci-Fi", "Sci-Fi"
        SHORT = "Short"
        THRILLER = "Thriller"
        WAR = "War"
        WESTERN = "Western"

    value = models.CharField(
        max_length=20,
        choices=Genres,
        default=Genres.DRAMA,
        verbose_name="Genre Value",
    )

    def __str__(self):
        return f"[{self.pk}] {self.value}"


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name="Company Name")

    def __str__(self):
        return f"[{self.pk}]: {self.name}"


class Movie(models.Model):
    title = models.CharField(max_length=100, verbose_name="Movie Title")
    year = models.IntegerField(
        default=current_year,
        validators=[validate_year],
        verbose_name="Year",
    )
    mpaa_rating = models.ForeignKey(
        MpaaRating, on_delete=models.PROTECT, verbose_name="Mpaa Rating"
    )
    cast = models.ManyToManyField(Actor, through="MovieActor")
    directors = models.ManyToManyField(Director)
    genres = models.ManyToManyField(Genre)
    companies = models.ManyToManyField(Company)

    class Meta:
        ordering: ClassVar[list[str]] = ["title", "year"]
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(
                fields=["title", "year"], name="unique_movie_title_year"
            ),
            models.CheckConstraint(
                condition=models.Q(year__gte=MIN_YEAR), name="movie_year_gte_min"
            ),
        ]

    def __str__(self):
        return f"[{self.pk}] {self.title} ({self.year})"

    def get_cleaned_title(self):
        pattern = re.compile(r", The$", re.IGNORECASE)
        if not pattern.search(self.title):
            return self.title
        return f"The {pattern.sub('', self.title)}"

    def avg_user_rating(self):
        return self.reviews.aggregate(Avg("rating"))["rating__avg"]


class Review(models.Model):
    class StarRatings(models.IntegerChoices):
        ONE = 1, "1-star"
        TWO = 2, "2-star"
        THREE = 3, "3-star"
        FOUR = 4, "4-star"
        FIVE = 5, "5-star"

    time = models.DateTimeField(auto_now_add=True, verbose_name="Time")
    user_name = models.CharField(max_length=20, verbose_name="User Name")
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="reviews", verbose_name="Movie"
    )
    rating = models.IntegerField(
        choices=StarRatings,
        default=StarRatings.FIVE,
        verbose_name="User Rating",
    )
    comment = models.TextField(max_length=2000, blank=True, default="")

    class Meta:
        ordering: ClassVar[list[str]] = ["-time"]
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.CheckConstraint(
                condition=models.Q(rating__range=(1, 5)), name="review_rating_1_to_5"
            ),
        ]

    def __str__(self):
        return f"[{self.pk}] movie:{self.movie_id} user:{self.user_name} time:{self.time} rating:{self.rating}"


class MovieActor(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Movie")
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, verbose_name="Actor")

    class Meta:
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(
                fields=["movie", "actor"], name="unique_movie_actor"
            ),
        ]

    def __str__(self):
        return f"[{self.pk}] movie={self.movie_id} actor={self.actor_id}"

    def roles(self):
        return self.movieactorrole_set.all().values_list("role", flat=True)


class MovieActorRole(models.Model):
    movie_actor = models.ForeignKey(MovieActor, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, verbose_name="Role")

    def __str__(self):
        return f"[{self.pk}] movie_actor={self.movie_actor_id} role={self.role}"
