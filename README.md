
MovieDB
==========


DESCRIPTION
------------
A simple movie database application using Python and the Django web framework.
Uses a SQLite backend.


AUTHOR
----------
James Gomez


REQUIREMENTS
-------------
* Python 3.12+
* Django 6.1 (see requirements.txt)


RUNNING
-------------
    uv venv && uv pip install -r requirements.txt
    .venv/bin/python manage.py migrate      # creates db.sqlite3 and loads the seed data
    .venv/bin/python manage.py runserver    # http://localhost:8000/MovieDB/
    .venv/bin/python manage.py test
