-- total cards in application table
drop table if exists cards;
CREATE TABLE cards (
    card_id INT PRIMARY KEY,
    name VARCHAR(20),

    -- 5 ranks in increasing rarity
    rank INT
);


-- user's collection of cards table
-- ownership table, card and user attribute as foreign keys
drop table if exists collection;
CREATE TABLE collection (
    card_id int,
    user_id int,
    FOREIGN KEY (card_id) REFERENCES cards,
    FOREIGN KEY (user_id) REFERENCES users
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
    user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    wallet_balance INT DEFAULT 500
);

drop table if exists friends;
CREATE TABLE friends (
    user1_id int,
    user2_id int,
    FOREIGN KEY (user1_id) REFERENCES users,
    FOREIGN KEY (user2_id) REFERENCES users
);