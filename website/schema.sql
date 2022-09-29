DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS upload;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL,
    featured INTEGER
);

CREATE TABLE upload (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uploader TEXT NOT NULL,
    upload_path TEXT NOT NULL,
    thumbnail_path TEXT NOT NULL,
    upload_name TEXT NOT NULL,
    kind TEXT NOT NULL,
    upload_time TIMESTAMP NOT NULL 
);

