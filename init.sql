CREATE USER docker;
CREATE DATABASE search_db;
GRANT ALL PRIVILEGES ON DATABASE search_db TO docker;

\connect search_db
CREATE SCHEMA IF NOT EXISTS snowy_search;

CREATE TABLE snowy_search.news (
    id SERIAL PRIMARY KEY UNIQUE ,
    url VARCHAR(510) NOT NULL,
    text VARCHAR NOT NULL,
    article_publish_date TIMESTAMP NOT NULL,
    article_insert_date TIMESTAMP NOT NULL DEFAULT NOW(),
    title_hash VARCHAR(24) NOT NULL UNIQUE
);

CREATE INDEX idx_title_hash
ON snowy_search.news(title_hash);