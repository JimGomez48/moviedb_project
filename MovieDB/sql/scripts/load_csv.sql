SET GLOBAL local_infile = 'ON';

LOAD DATA LOCAL INFILE 'MovieDB/sql/seeds/csv/actor1.csv' INTO TABLE actors
    FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
    (id, last, first, sex, dob, dod);
LOAD DATA LOCAL INFILE 'MovieDB/sql/seeds/csv/actor2.csv' INTO TABLE actors
    FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
    (id, last, first, sex, dob, dod);
LOAD DATA LOCAL INFILE 'MovieDB/sql/seeds/csv/actor3.csv' INTO TABLE actors
    FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
    (id, last, first, sex, dob, dod);

LOAD DATA LOCAL INFILE 'MovieDB/sql/seeds/csv/company.csv' INTO TABLE companies
    FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
    (id, name);

LOAD DATA LOCAL INFILE 'MovieDB/sql/seeds/csv/director.csv' INTO TABLE directors
    FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
    (id, last, first, dob, dod);

LOAD DATA LOCAL INFILE 'MovieDB/sql/seeds/csv/movie.csv' INTO TABLE movies
    FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
    (id, title, year, mpaa_rating_id);

SET FOREIGN_KEY_CHECKS = 0;

LOAD DATA LOCAL INFILE 'MovieDB/sql/seeds/csv/movieactor1.csv' INTO TABLE movie_actors
    FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
    (movie_id, actor_id);
LOAD DATA LOCAL INFILE 'MovieDB/sql/seeds/csv/movieactor2.csv' INTO TABLE movie_actors
    FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
    (movie_id, actor_id);

LOAD DATA LOCAL INFILE 'MovieDB/sql/seeds/csv/movieactorrole1.csv' INTO TABLE movie_actor_roles
    FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
    (movie_actor_id, role);
LOAD DATA LOCAL INFILE 'MovieDB/sql/seeds/csv/movieactorrole2.csv' INTO TABLE movie_actor_roles
    FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
    (movie_actor_id, role);

LOAD DATA LOCAL INFILE 'MovieDB/sql/seeds/csv/moviecompany.csv' INTO TABLE movie_companies
    FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
    (movie_id, company_id);

LOAD DATA LOCAL INFILE 'MovieDB/sql/seeds/csv/moviedirector.csv' INTO TABLE movie_directors
    FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
    (@dummy, movie_id, director_id);

LOAD DATA LOCAL INFILE 'MovieDB/sql/seeds/csv/moviegenre.csv' INTO TABLE movie_genres
    FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
    (@dummy, movie_id, genre_id);

SET FOREIGN_KEY_CHECKS = 1;
