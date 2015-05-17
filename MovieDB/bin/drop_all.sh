#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

mysql --user=james --password=pennies48 --local-infile --execute="DROP DATABASE movie_db;"
echo "Dropped database 'movie_db'"