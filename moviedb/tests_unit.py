from datetime import date

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from moviedb import models


class TestModels(TestCase):
    def test_select_related_movieactor_actor(self):
        results = models.MovieActor.objects.filter(movie_id=253).select_related("actor")
        self.assertTrue(results.exists())
        for item in results:
            self.assertTrue(item.actor.get_full_name())

    def test_cleaned_movie_title(self):
        manager = models.Movie.objects
        # a movie NOT starting with 'The'
        movie = manager.get(id=2)
        self.assertEqual(movie.title, movie.get_cleaned_title())
        # a movie starting with 'The', thus stored with ', The' at the end
        movie = manager.get(id=9)
        self.assertEqual("The 13th Warrior", movie.get_cleaned_title())

    def test_avg_user_rating(self):
        self.assertAlmostEqual(
            11 / 3.0, models.Movie.objects.get(id=253).avg_user_rating()
        )


class TestValidation(TestCase):
    def test_actor_death_before_birth_is_a_field_error(self):
        actor = models.Actor(
            last="A", first="B", sex="male", dob=date(2000, 1, 1), dod=date(1999, 1, 1)
        )
        with self.assertRaises(ValidationError) as ctx:
            actor.full_clean()
        self.assertEqual(["dod"], list(ctx.exception.error_dict))

    def test_actor_death_before_birth_rejected_by_db(self):
        actor = models.Actor(
            last="A", first="B", sex="male", dob=date(2000, 1, 1), dod=date(1999, 1, 1)
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            actor.save()

    def test_actor_without_death_date_is_valid(self):
        actor = models.Actor(last="A", first="B", sex="male", dob=date(2000, 1, 1))
        actor.full_clean()
        actor.save()

    def test_director_death_before_birth_rejected_by_db(self):
        director = models.Director(
            last="A", first="B", dob=date(2000, 1, 1), dod=date(1999, 1, 1)
        )
        with self.assertRaises(ValidationError):
            director.full_clean()
        with self.assertRaises(IntegrityError), transaction.atomic():
            director.save()

    def test_movie_year_bounds(self):
        for year in (models.MIN_YEAR - 1, models.current_year() + 1):
            movie = models.Movie(title="X", year=year, mpaa_rating_id=1)
            with self.assertRaises(ValidationError) as ctx:
                movie.full_clean()
            self.assertIn("year", ctx.exception.error_dict)

    def test_movie_year_floor_rejected_by_db(self):
        movie = models.Movie(title="X", year=models.MIN_YEAR - 1, mpaa_rating_id=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            movie.save()

    def test_review_rating_range(self):
        review = models.Review(user_name="u", movie_id=253, rating=6)
        with self.assertRaises(ValidationError) as ctx:
            review.full_clean()
        self.assertIn("rating", ctx.exception.error_dict)
        with self.assertRaises(IntegrityError), transaction.atomic():
            review.save()


class TestLinkTables(TestCase):
    def test_movie_actor_duplicate_rejected(self):
        models.MovieActor.objects.create(movie_id=253, actor_id=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            models.MovieActor.objects.create(movie_id=253, actor_id=1)

    def test_plain_many_to_many_adds_are_idempotent(self):
        movie = models.Movie.objects.get(id=253)
        for field, related in (
            ("directors", models.Director.objects.first()),
            ("genres", models.Genre.objects.first()),
            ("companies", models.Company.objects.first()),
        ):
            manager = getattr(movie, field)
            manager.add(related)
            manager.add(related)
            self.assertEqual(1, manager.filter(pk=related.pk).count(), field)

    def test_seed_data_loads_link_tables(self):
        self.assertEqual(1119, models.Movie.directors.through.objects.count())
        self.assertEqual(5972, models.Movie.genres.through.objects.count())
        self.assertEqual(3616, models.Movie.companies.through.objects.count())
