CREATE DATABASE post_db;

CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(40) UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    avatar TEXT
);

CREATE TABLE posts(
    post_id SERIAL PRIMARY KEY,
    title VARCHAR(40) NOT NULL,
    description TEXT,
    post_image TEXT,
    user_id SERIAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);