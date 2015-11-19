#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

echo "Creating 'movie_db' database..."
mysql --user=james --password=test --local-infile --execute="CREATE DATABASE movie_db;"

echo "Starting migration..."
cd ~/Documents/django_workspace/moviedb_project/
python manage.py makemigrations
python manage.py migrate

cd ~/Documents/django_workspace/moviedb_project/MovieDB/sql/scripts/
echo "Loading seed data..."
mysql --user=james --password=test movie_db --local-infile < load.sql

cd ~/Documents/django_workspace/moviedb_project
echo "DONE"