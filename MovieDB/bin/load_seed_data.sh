#!/usr/bin/env bash
SCRIPT_PATH=MovieDB/sql/scripts/load.sql
echo "Loading seed data..."
mysql --user=james --password=test movie_db --local-infile < $SCRIPT_PATH


