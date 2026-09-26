from django.test import TestCase
from django.urls import reverse

from moviedb import models


class TestPages(TestCase):
    def assert_ok(self, name, *args):
        response = self.client.get(reverse(name, args=args))
        self.assertEqual(200, response.status_code, name)
        return response

    def test_index(self):
        self.assert_ok("Index")

    def test_browse_pages(self):
        for name in ("BrowseMovie", "BrowseActor", "BrowseDirector"):
            self.assert_ok(name)

    def test_detail_pages(self):
        movie_actor = models.MovieActor.objects.first()
        self.assert_ok("MovieDetail", 253)
        self.assert_ok("ActorDetail", movie_actor.actor_id)
        self.assert_ok(
            "DirectorDetail", models.MovieDirector.objects.first().director_id
        )

    def test_add_forms(self):
        for name in (
            "AddMovie",
            "AddActorDirector",
            "AddActorMovie",
            "AddDirectorMovie",
            "WriteReview",
        ):
            self.assert_ok(name)


class TestWrites(TestCase):
    def test_write_review(self):
        before = models.Review.objects.count()
        response = self.client.post(
            reverse("WriteReview"),
            {"user_name": "tester", "movie": 253, "rating": 4, "comment": "ok"},
        )
        self.assertEqual(302, response.status_code)
        self.assertEqual(before + 1, models.Review.objects.count())

    def test_add_movie_rejects_duplicate(self):
        data = {
            "submit": "movie",
            "title": "Zed",
            "year": 2000,
            "mpaa_rating": 1,
            "genres": ["Drama"],
        }
        self.assertEqual(302, self.client.post(reverse("AddMovie"), data).status_code)
        self.assertEqual(200, self.client.post(reverse("AddMovie"), data).status_code)
        self.assertEqual(1, models.Movie.objects.filter(title="Zed").count())

    def test_add_actor_with_death_before_birth_shows_form_error(self):
        response = self.client.post(
            reverse("AddActorDirector"),
            {
                "submit": "actor",
                "last": "Zzqx",
                "first": "Q",
                "sex": "male",
                "dob": "01/02/1980",
                "dod": "01/02/1970",
            },
        )
        self.assertEqual(200, response.status_code)
        self.assertFalse(models.Actor.objects.filter(last="Zzqx").exists())

    def test_add_same_actor_to_movie_twice_shows_form_error(self):
        data = {"movie": 253, "actor": 1}
        self.assertEqual(
            302, self.client.post(reverse("AddActorMovie"), data).status_code
        )
        self.assertEqual(
            200, self.client.post(reverse("AddActorMovie"), data).status_code
        )
        self.assertEqual(
            1, models.MovieActor.objects.filter(movie_id=253, actor_id=1).count()
        )

    def test_add_same_director_to_movie_twice_shows_form_error(self):
        data = {"movie": 253, "director": 37146}
        self.assertEqual(
            302, self.client.post(reverse("AddDirectorMovie"), data).status_code
        )
        self.assertEqual(
            200, self.client.post(reverse("AddDirectorMovie"), data).status_code
        )
