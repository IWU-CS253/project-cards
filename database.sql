-- total cards in application table
drop table if exists cards;
CREATE TABLE cards (
    card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100),

    -- 5 ranks in increasing rarity
    rank INT
);


-- user's collection of cards table
-- ownership table, card and user attribute as foreign keys
drop table if exists collection;
CREATE TABLE collection (
    delete_id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id INT,
    user_id INT,
    image VARCHAR(150),
    FOREIGN KEY (card_id) REFERENCES cards,
    FOREIGN KEY (user_id) REFERENCES users,
    FOREIGN KEY (image) REFERENCES store
);

-- cards to be shown in the store table
drop table if exists store;
CREATE TABLE store (
    card_id INT,
    rank VARCHAR(10),
    image VARCHAR(150),
    pack1 BOOL,
    pack2 BOOL,
    pack3 BOOL,
    pack4 BOOL,
    pack5 BOOL,
    pack6 BOOL,
    pack7 BOOL
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
    user_id INT,
    card_id INT,
    wallet_change INT NOT NULL,
    FOREIGN KEY (card_id) REFERENCES cards,
    FOREIGN KEY (user_id) REFERENCES users
);

drop table if exists trades;
CREATE TABLE trades (
    trade_id INT,
    request_id INT,
    offer_id INT,
    card_id INT,
    delete_id INT,
    FOREIGN KEY (card_id) REFERENCES cards,
    FOREIGN KEY (offer_id) REFERENCES users,
    FOREIGN KEY (request_id) REFERENCES users,
    FOREIGN KEY (delete_id) REFERENCES collection
);

drop table if exists marketplace;
CREATE TABLE marketplace (
    market_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT,
    card_id INT,
    name VARCHAR(100),
    price INT,
    FOREIGN KEY (card_id) REFERENCES cards,
    FOREIGN KEY (user_id) REFERENCES users,
    FOREIGN KEY (name) REFERENCES cards
);

