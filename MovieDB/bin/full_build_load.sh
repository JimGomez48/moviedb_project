#!/usr/bin/env bash

USR='jgomez'
PWD='test'

BASE_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

echo "Creating 'movie_db' database..."
mysql -u $USR --password=$PWD --local-infile --execute="CREATE DATABASE movie_db;"

echo "Starting migration..."
cd $BASE_DIR/../..
python manage.py makemigrations
python manage.py migrate

cd ./MovieDB/sql/scripts/
echo "Loading seed data..."
mysql -u $USR --password=$PWD movie_db --local-infile < load_csv.sql

cd $BASE_DIR
echo "DONE"