SET GLOBAL local_infile=1;

LOAD DATA LOCAL INFILE './seed_data/actor1.del' INTO TABLE MovieDB_actor FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"';
LOAD DATA LOCAL INFILE './seed_data/actor2.del' INTO TABLE MovieDB_actor FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"';
LOAD DATA LOCAL INFILE './seed_data/actor3.del' INTO TABLE MovieDB_actor FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"';

LOAD DATA LOCAL INFILE './seed_data/director.del' INTO TABLE MovieDB_director FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"';

LOAD DATA LOCAL INFILE './seed_data/movie.del' INTO TABLE MovieDB_movie FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"';

LOAD XML LOCAL INFILE './seed_data/movieactor1.xml' INTO TABLE MovieDB_movieactor;
LOAD XML LOCAL INFILE './seed_data/movieactor2.xml' INTO TABLE MovieDB_movieactor;

LOAD XML LOCAL INFILE './seed_data/moviedirector.xml' INTO TABLE MovieDB_moviedirector;

LOAD XML LOCAL INFILE './seed_data/moviegenre.xml' INTO TABLE MovieDB_moviegenre;

INSERT INTO MovieDB_maxpersonid VALUES (69000);
INSERT INTO MovieDB_maxmovieid VALUES (4750);