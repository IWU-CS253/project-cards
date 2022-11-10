
-- total cards in application table
drop table if exists cards;
CREATE TABLE cards (
    card_id INT PRIMARY KEY,
    name VARCHAR(20),

    -- 5 ranks in increasing rarity
    rank INT
);


-- user's collection of cards table
drop table if exists collection;
CREATE TABLE collection (
    card_id INT,
    name VARCHAR(20),
    rank INT
);

-- cards to be shown in the store table
drop table if exists store;
CREATE TABLE store (
    card_id INT,
    name VARCHAR(20),
    rank INT,
    price INT
);

drop table if exists users;
CREATE TABLE users (
    numeric_id INT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);