import csv
import datetime
import os

from django.db import migrations

from moviedb_project.settings import BASE_DIR


def load_static_tables(apps, schema_editor):
    # load mpaa_ratings
    MpaaRating = apps.get_model("MovieDB", "MpaaRating")
    MpaaRating.objects.bulk_create(
        [
            MpaaRating(value="G"),
            MpaaRating(value="PG"),
            MpaaRating(value="PG-13"),
            MpaaRating(value="R"),
            MpaaRating(value="NC-17"),
            MpaaRating(value="surrendered"),
        ]
    )
    # load genres
    Genre = apps.get_model("MovieDB", "Genre")
    Genre.objects.bulk_create(
        [
            Genre(value="Action"),
            Genre(value="Adult"),
            Genre(value="Adventure"),
            Genre(value="Animation"),
            Genre(value="Crime"),
            Genre(value="Comedy"),
            Genre(value="Documentary"),
            Genre(value="Drama"),
            Genre(value="Family"),
            Genre(value="Fantasy"),
            Genre(value="Horror"),
            Genre(value="Musical"),
            Genre(value="Mystery"),
            Genre(value="Romance"),
            Genre(value="Sci-Fi"),
            Genre(value="Short"),
            Genre(value="Thriller"),
            Genre(value="War"),
            Genre(value="Western"),
        ]
    )


SEED_DIR = os.path.join(BASE_DIR, "MovieDB", "sql", "seeds", "csv")
BATCH_SIZE = 2000


def _read_csv(name):
    """Yield rows of a seed csv; MySQL's \\N null marker becomes None."""
    with open(os.path.join(SEED_DIR, name), newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            yield [None if v == "\\N" else v for v in row]


def _date(value):
    return datetime.datetime.strptime(value, "%Y%m%d").date() if value else None


def _load(model, names, fields):
    """Bulk-load csv files; fields is a list of (attname, converter or None)."""
    batch = []
    for name in names:
        for row in _read_csv(name):
            values = {}
            for (attr, convert), value in zip(fields, row):
                if attr is None:
                    continue
                values[attr] = convert(value) if convert else value
            batch.append(model(**values))
            if len(batch) >= BATCH_SIZE:
                model.objects.bulk_create(batch)
                batch = []
    if batch:
        model.objects.bulk_create(batch)


def load_seed_data(apps, schema_editor):
    print("Loading seed data...")
    m = apps.get_model
    _load(
        m("MovieDB", "Actor"),
        ["actor1.csv", "actor2.csv", "actor3.csv"],
        [
            ("id", int),
            ("last", None),
            ("first", None),
            ("sex", None),
            ("dob", _date),
            ("dod", _date),
        ],
    )
    _load(m("MovieDB", "Company"), ["company.csv"], [("id", int), ("name", None)])
    _load(
        m("MovieDB", "Director"),
        ["director.csv"],
        [("id", int), ("last", None), ("first", None), ("dob", _date), ("dod", _date)],
    )
    _load(
        m("MovieDB", "Movie"),
        ["movie.csv"],
        [("id", int), ("title", None), ("year", int), ("mpaa_rating_id", int)],
    )
    # link tables: ids are auto-assigned, so the row order defines them (as with LOAD DATA)
    _load(
        m("MovieDB", "MovieActor"),
        ["movieactor1.csv", "movieactor2.csv"],
        [("movie_id", int), ("actor_id", int)],
    )
    _load(
        m("MovieDB", "MovieActorRole"),
        ["movieactorrole1.csv", "movieactorrole2.csv"],
        [("movie_actor_id", int), ("role", None)],
    )
    _load(
        m("MovieDB", "MovieCompany"),
        ["moviecompany.csv"],
        [("movie_id", int), ("company_id", int)],
    )
    _load(
        m("MovieDB", "MovieDirector"),
        ["moviedirector.csv"],
        [(None, None), ("movie_id", int), ("director_id", int)],
    )
    _load(
        m("MovieDB", "MovieGenre"),
        ["moviegenre.csv"],
        [(None, None), ("movie_id", int), ("genre_id", int)],
    )


def load_seed_reviews(apps, schema_editor):
    Review = apps.get_model("MovieDB", "Review")
    Movie = apps.get_model("MovieDB", "Movie")
    Review.objects.bulk_create(
        [
            Review(
                time="2015-11-23 05:35:35",
                user_name="Jim",
                movie=Movie.objects.get(id=253),
                rating=5,
                comment="Great!",
            ),
            Review(
                time="2015-11-23 05:35:35",
                user_name="James",
                movie=Movie.objects.get(id=253),
                rating=2,
                comment="Ehh...",
            ),
            Review(
                time="2015-11-23 05:35:35",
                user_name="Jimbo",
                movie=Movie.objects.get(id=253),
                rating=4,
                comment="Pretty good",
            ),
        ]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("MovieDB", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_static_tables),
        migrations.RunPython(load_seed_data),
        migrations.RunPython(load_seed_reviews),
    ]
