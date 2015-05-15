CREATE TABLE Movie(
    id INT NOT NULL, 
    title VARCHAR(100) NOT NULL,
    year INT, 
    rating VARCHAR(10),
    company VARCHAR(50),
    PRIMARY KEY(id),
    UNIQUE (title, year),
    UNIQUE (title, company),
    CHECK (
        rating='G' OR rating='PG' OR rating='PG-13' OR 
        rating='R' OR rating='NC-17' OR rating='surrendere')
)
ENGINE = "INNODB";

CREATE TABLE Actor(
    id INT NOT NULL,
    last VARCHAR(20) NOT NULL,
    first VARCHAR(20) NOT NULL,
    sex VARCHAR(6) NOT NULL,
    dob DATE NOT NULL,
    dod DATE,
    PRIMARY KEY(id),
    UNIQUE (last, first, dob),
    CHECK (dob < dod)
)
ENGINE = "INNODB";

CREATE TABLE Director(
    id INT NOT NULL,
    last VARCHAR(20) NOT NULL,
    first VARCHAR(20) NOT NULL,
    dob DATE NOT NULL,
    dod DATE,
    PRIMARY KEY(id),
    UNIQUE (last, first, dob),
    CHECK (dob < dod)
)
ENGINE = "INNODB";

CREATE TABLE MovieGenre(
    mid INT NOT NULL,
    genre VARCHAR(20) NOT NULL,
    PRIMARY KEY(mid, genre),
    FOREIGN KEY(mid) REFERENCES Movie(id)
)
ENGINE = "INNODB";

CREATE TABLE MovieDirector(
    mid INT NOT NULL,
    did INT NOT NULL,
    PRIMARY KEY(mid, did),
    FOREIGN KEY(mid) REFERENCES Movie(id),
    FOREIGN KEY(did) REFERENCES Director(id)
)
ENGINE = "INNODB";

CREATE TABLE MovieActor(
    mid INT NOT NULL,
    aid INT NOT NULL,
    role VARCHAR(50) NOT NULL,
    PRIMARY KEY(mid, aid, role),
    UNIQUE(mid, aid),
    FOREIGN KEY(mid) REFERENCES Movie(id),
    FOREIGN KEY(aid) REFERENCES Actor(id)
)
ENGINE = "INNODB";

CREATE TABLE Review(
    name VARCHAR(20) NOT NULL,
    time TIMESTAMP NOT NULL,
    mid INT NOT NULL,
    rating INT NOT NULL,
    comment VARCHAR(500),
    PRIMARY KEY(name, mid),
    CHECK (1 <= rating <= 5),
    FOREIGN KEY(mid) REFERENCES Movie(id)
)
ENGINE = "INNODB";

-- Can't enforce foreign key constraint on two tables below. Can be a foreign 
-- key to either Actor or Director table, but never boths. Also, data and 
-- starting maxes do not match.
CREATE TABLE MaxPersonID(
    id INT NOT NULL
    -- CHECK ((SELECT count(*) FROM MaxPersonID)<=1)
)
ENGINE = "INNODB";

CREATE TABLE MaxMovieID(
    id INT NOT NULL
    -- CHECK ((SELECT count(*) FROM MaxMovieID)<=1)
)
ENGINE = "INNODB";