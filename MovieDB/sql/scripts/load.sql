SET GLOBAL local_infile = 'ON';

# LOAD XML LOCAL INFILE 'MovieDB/sql/seed_data/xml/actor1.xml' INTO TABLE MovieDB_actor CHARACTER SET UTF8;
# LOAD XML LOCAL INFILE 'MovieDB/sql/seed_data/xml/actor2.xml' INTO TABLE MovieDB_actor CHARACTER SET UTF8;
# LOAD XML LOCAL INFILE 'MovieDB/sql/seed_data/xml/actor3.xml' INTO TABLE MovieDB_actor CHARACTER SET UTF8;
#
# LOAD XML LOCAL INFILE 'MovieDB/sql/seed_data/xml/director.xml' INTO TABLE MovieDB_director CHARACTER SET UTF8;
#
# LOAD XML LOCAL INFILE 'MovieDB/sql/seed_data/xml/movie.xml' INTO TABLE MovieDB_movie CHARACTER SET UTF8;
#
# LOAD XML LOCAL INFILE 'MovieDB/sql/seed_data/xml/movieactor1.xml' INTO TABLE MovieDB_movieactor CHARACTER SET UTF8;
# LOAD XML LOCAL INFILE 'MovieDB/sql/seed_data/xml/movieactor2.xml' INTO TABLE MovieDB_movieactor CHARACTER SET UTF8;
#
# LOAD XML LOCAL INFILE 'MovieDB/sql/seed_data/xml/moviedirector.xml' INTO TABLE MovieDB_moviedirector CHARACTER SET UTF8;
#
# LOAD XML LOCAL INFILE 'MovieDB/sql/seed_data/xml/moviegenre.xml' INTO TABLE MovieDB_moviegenre CHARACTER SET UTF8;


LOAD DATA LOCAL INFILE 'MovieDB/sql/seed_data/csv/actor1.del' INTO TABLE Actors FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
LOAD DATA LOCAL INFILE 'MovieDB/sql/seed_data/csv/actor2.del' INTO TABLE Actors FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
LOAD DATA LOCAL INFILE 'MovieDB/sql/seed_data/csv/actor3.del' INTO TABLE Actors FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';

LOAD DATA LOCAL INFILE 'MovieDB/sql/seed_data/csv/director.del' INTO TABLE Directors FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';

LOAD DATA LOCAL INFILE 'MovieDB/sql/seed_data/csv/movie.del' INTO TABLE Movies FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';

SET FOREIGN_KEY_CHECKS = 0;

LOAD DATA LOCAL INFILE 'MovieDB/sql/seed_data/csv/movieactor1.del' INTO TABLE MovieActors FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
LOAD DATA LOCAL INFILE 'MovieDB/sql/seed_data/csv/movieactor2.del' INTO TABLE MovieActors FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';

LOAD DATA LOCAL INFILE 'MovieDB/sql/seed_data/csv/moviedirector.del' INTO TABLE MovieDirectors FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';

LOAD DATA LOCAL INFILE 'MovieDB/sql/seed_data/csv/moviegenre.del' INTO TABLE MovieGenres FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';

SET FOREIGN_KEY_CHECKS = 1;
