#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

cd ~/Documents/django_workspace/moviedb_project/
python manage.py makemigrations
python manage.py migrate

cd ~/Documents/django_workspace/moviedb_project/MovieDB/sql/scripts/
echo "Loading seed data..."
mysql --user=james --password=pennies48 movie_db --local-infile < load.sql

cd ~/Documents/django_workspace/moviedb_project
echo "DONE"