@echo on
echo Loading seed data...
mysql --user=james --password=test movie_db --local-infile < "MovieDB/sql/scripts/load.sql"