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

    last = models.CharField(
        max_length=50, blank=False, null=False, verbose_name="Last Name"
    )
    first = models.CharField(
        max_length=50, blank=False, null=False, verbose_name="First Name"
    )
    sex = models.CharField(
        max_length=6, choices=Sex, blank=False, null=False, verbose_name="Sex"
    )
    dob = models.DateField(verbose_name="Date of Birth")
    dod = models.DateField(
        null=True, blank=True, default=None, verbose_name="Date of Death"
    )

    class Meta:
        db_table = "actors"
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
    last = models.CharField(
        max_length=20, blank=False, null=False, verbose_name="Last Name"
    )
    first = models.CharField(
        max_length=20, blank=False, null=False, verbose_name="First Name"
    )
    dob = models.DateField(blank=False, null=False, verbose_name="Date of Birth")
    dod = models.DateField(
        null=True, blank=True, default=None, verbose_name="Date of Death"
    )

    class Meta:
        db_table = "directors"
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
    class Value(models.TextChoices):
        NC_17 = "NC-17", "NC-17"
        R = "R", "R"
        PG_13 = "PG-13", "PG-13"
        PG = "PG", "PG"
        G = "G", "G"
        SURRENDERED = "surrendered", "Not Rated"

    value = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        choices=Value,
        verbose_name="Mpaa Rating Value",
    )

    class Meta:
        db_table = "mpaa_ratings"

    def __str__(self):
        return f"[{self.pk}] {self.value}"


class Genre(models.Model):
    class Value(models.TextChoices):
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
        choices=Value,
        blank=False,
        null=False,
        default=Value.DRAMA,
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
        blank=False,
        null=False,
        default=current_year,
        validators=[validate_year],
        verbose_name="Year",
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
            models.CheckConstraint(
                condition=models.Q(year__gte=MIN_YEAR), name="movie_year_gte_min"
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


class Review(models.Model):
    class Rating(models.IntegerChoices):
        ONE = 1, "1-star"
        TWO = 2, "2-star"
        THREE = 3, "3-star"
        FOUR = 4, "4-star"
        FIVE = 5, "5-star"

    time = models.DateTimeField(auto_now=True, editable=False, verbose_name="Time")
    user_name = models.CharField(
        max_length=20, blank=False, null=False, verbose_name="User Name"
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Movie")
    rating = models.IntegerField(
        choices=Rating,
        blank=False,
        null=False,
        default=Rating.FIVE,
        verbose_name="User Rating",
    )
    comment = models.TextField(max_length=2000, blank=True, default="")

    class Meta:
        db_table = "reviews"
        ordering: ClassVar[list[str]] = ["-time"]
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.CheckConstraint(
                condition=models.Q(rating__range=(1, 5)), name="review_rating_1_to_5"
            ),
        ]

    def __str__(self):
        return f"[{self.pk}] movie:{self.movie.pk} user:{self.user_name} time:{self.time} rating:{self.rating}"


class MovieCompany(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Movie")
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, verbose_name="Company"
    )

    class Meta:
        db_table = "movie_companies"
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(
                fields=["movie", "company"], name="unique_movie_company"
            ),
        ]

    def __str__(self):
        return f"[{self.pk}] movie={self.movie.pk} company={self.company.pk}"


class MovieActor(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Movie")
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, verbose_name="Actor")

    class Meta:
        db_table = "movie_actors"
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(
                fields=["movie", "actor"], name="unique_movie_actor"
            ),
        ]

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
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(
                fields=["movie", "director"], name="unique_movie_director"
            ),
        ]

    def __str__(self):
        return f"[{self.pk}] movie={self.movie.pk} director={self.director.pk}"


class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Movie")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name="Movie")

    class Meta:
        db_table = "movie_genres"
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(
                fields=["movie", "genre"], name="unique_movie_genre"
            ),
        ]

    def __str__(self):
        return f"[{self.pk}] movie={self.movie.pk} genre={self.genre.pk}"
