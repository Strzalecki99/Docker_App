CREATE TABLE movies (
    movieId INT PRIMARY KEY,
    title TEXT,
    genres TEXT
);

CREATE TABLE ratings (
    ratingId SERIAL PRIMARY KEY,
    userId INT,
    movieId INT,
    rating FLOAT,
    timestamp BIGINT
);

COPY movies(movieId, title, genres)
FROM '/mnt/data/movies.csv'
DELIMITER ',' CSV HEADER;

COPY ratings(userId, movieId, rating, timestamp)
FROM '/mnt/data/ratings.csv'
DELIMITER ',' CSV HEADER;