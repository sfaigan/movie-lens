-- Entities
CREATE TABLE users (id int NOT NULL PRIMARY KEY);

CREATE TABLE tags (
    id int NOT NULL PRIMARY KEY,
    name varchar NOT NULL
);

CREATE TABLE movies (
    id int NOT NULL PRIMARY KEY,
    name varchar NOT NULL
);

CREATE TABLE genres (name varchar NOT NULL PRIMARY KEY);

-- Relations
-- User APPLIES a Tag to a Movie
CREATE TABLE applies (
    userId int NOT NULL,
    movieId int NOT NULL,
    tagId int NOT NULL,
    -- timestamp timestamp NOT NULL,
    PRIMARY KEY (userId, tagId, movieId),
    FOREIGN KEY (userId) REFERENCES users(id),
    FOREIGN KEY (tagId) REFERENCES tags(id),
    FOREIGN KEY (movieId) REFERENCES movies(id)
);

-- Movie RELATES_TO a Tag
CREATE TABLE relates_to (
    movieId int NOT NULL,
    tagId int NOT NULL,
    relevance float NOT NULL CHECK (relevance >= 0 AND relevance <= 1),
    PRIMARY KEY (movieId, tagId),
    FOREIGN KEY (movieId) REFERENCES movies(id),
    FOREIGN KEY (tagId) REFERENCES tags(id)
);

-- Movie IS_CATEGORIZED_AS a Genre
CREATE TABLE is_categorized_as (
    movieId int NOT NULL,
    genreName varchar NOT NULL,
    PRIMARY KEY (movieId, genreName),
    FOREIGN KEY (movieId) REFERENCES movies(id),
    FOREIGN KEY (genreName) REFERENCES genres(name)
);

-- User RATES a Movie
CREATE TABLE rates (
    userId int NOT NULL,
    movieId int NOT NULL,
    rating float NOT NULL CHECK (rating >= 0 AND rating <= 5),
    -- timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, -- May want to remove the default
    PRIMARY KEY (userId, movieId),
    FOREIGN KEY (userId) REFERENCES users(id),
    FOREIGN KEY (movieId) REFERENCES movies(id)
);
