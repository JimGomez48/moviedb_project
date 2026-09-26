from django.test import TestCase

from MovieDB import models


class TestModels(TestCase):
    def test_select_related_movieactor_actor(self):
        results = models.MovieActor.objects.filter(movie_id=253).select_related('actor')
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
        self.assertEqual('The 13th Warrior', movie.get_cleaned_title())

    def test_avg_user_rating(self):
        self.assertAlmostEqual(11 / 3.0, models.Movie.objects.get(id=253).avg_user_rating())
