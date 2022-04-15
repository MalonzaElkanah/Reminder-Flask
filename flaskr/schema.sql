DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS reminder_category;
DROP TABLE IF EXISTS reminder;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
    country_code TEXT,
    phone_number TEXT,
    email TEXT,
);

CREATE TABLE reminder_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT UNIQUE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE reminder (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT UNIQUE NOT NULL,
    event_date TIMESTAMP NOT NULL,
    reminder_date TIMESTAMP NOT NULL,
    repeat TEXT NOT NULL DEFAULT 'NONE',
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    location TEXT,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (category_id) REFERENCES reminder_category (id),
);
