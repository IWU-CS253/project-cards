-- total cards in application table
CREATE TABLE cards (
    card_id INT PRIMARY KEY,
    name VARCHAR(20),
    rank INT,
    type VARCHAR(5),
    pack VARCHAR(10),
    amount INT
);

-- user's collection of cards table
CREATE TABLE collection (
    card_id INT,
    name VARCHAR(20),
    rank INT
);

-- cards to be shown in the store table
CREATE TABLE store (
    card_id INT,
    name VARCHAR(20),
    rank INT,
    price INT
);
