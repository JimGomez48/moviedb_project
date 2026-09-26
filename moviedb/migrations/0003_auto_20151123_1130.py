from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("moviedb", "0002_sprocs_seeds"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="cast",
            field=models.ManyToManyField(
                to="moviedb.Actor", through="moviedb.MovieActor"
            ),
        ),
        migrations.AddField(
            model_name="movie",
            name="companies",
            field=models.ManyToManyField(
                to="moviedb.Company", through="moviedb.MovieCompany"
            ),
        ),
        migrations.AddField(
            model_name="movie",
            name="directors",
            field=models.ManyToManyField(
                to="moviedb.Director", through="moviedb.MovieDirector"
            ),
        ),
        migrations.AddField(
            model_name="movie",
            name="genres",
            field=models.ManyToManyField(
                to="moviedb.Genre", through="moviedb.MovieGenre"
            ),
        ),
    ]
