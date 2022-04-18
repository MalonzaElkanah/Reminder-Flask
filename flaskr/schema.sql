DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS reminder;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    country_code TEXT,
    phone_number TEXT,
    email TEXT
);

CREATE TABLE reminder (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT UNIQUE NOT NULL,
    reminder_date TIMESTAMP NOT NULL,
    repeat TEXT NOT NULL DEFAULT 'NONE',
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES user (id)
);
