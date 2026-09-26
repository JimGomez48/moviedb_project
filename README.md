
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
* [uv](https://docs.astral.sh/uv/) (manages Python and dependencies)
* Python 3.12+ (uv will install it if needed)
* Django 6.1 (declared in pyproject.toml, locked in uv.lock)


RUNNING
-------------
    uv sync                                # creates .venv and installs locked dependencies
    uv run manage.py migrate               # creates db.sqlite3 and loads the seed data
    uv run manage.py runserver             # dev server, http://localhost:8000/MovieDB/
    uv run uvicorn moviedb_project.asgi:application   # ASGI server (does not serve /static/)
    uv run manage.py test


DEPENDENCIES
-------------
    uv add <package>                       # add a runtime dependency
    uv add --dev <package>                 # add a dev dependency (pytest, ruff, ty, ...)
    uv lock --upgrade                      # upgrade locked versions

Dev tools (`ruff`, `ty`, `pytest`) are in the `dev` dependency group and are
installed by `uv sync`.
