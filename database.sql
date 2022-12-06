-- total cards in application table
drop table if exists cards;
CREATE TABLE cards (
    card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(20),

    -- 5 ranks in increasing rarity
    rank INT,
    price INT
);


-- user's collection of cards table
-- ownership table, card and user attribute as foreign keys
drop table if exists collection;
CREATE TABLE collection (
    delete_id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id INT,
    user_id INT,
    FOREIGN KEY (card_id) REFERENCES cards,
    FOREIGN KEY (user_id) REFERENCES users
);





-- cards to be shown in the store table
drop table if exists store;
CREATE TABLE store (
    card_id INT,
    rank VARCHAR(10),
    image VARCHAR(150),
    pack VARCHAR(10),
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

drop table if exists transactions;
CREATE TABLE transactions (
    user_id INT PRIMARY KEY,
    card_id INT,
    wallet_change INT NOT NULL,
    FOREIGN KEY (card_id) REFERENCES cards,
    FOREIGN KEY (user_id) REFERENCES users
);