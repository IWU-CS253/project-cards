CREATE TABLE cards (
    card_id INT PRIMARY KEY,
    name VARCHAR(20),
    rank INT,
    type VARCHAR(5),
    pack VARCHAR(10),
    amount INT
);

CREATE TABLE collection (
    card_id INT,
    name VARCHAR(20),
    rank INT
);

CREATE TABLE store (
    card_id INT,
    name VARCHAR(20),
    rank INT,
    price INT
);