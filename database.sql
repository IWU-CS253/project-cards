-- total cards in application table
CREATE TABLE cards (
    card_id INT PRIMARY KEY,
    name VARCHAR(20),

    -- 5 ranks in increasing rarity
    rank INT
);

-- pack of 51 cards with a food theme
.import 'FOOD_PACK.csv' cards --csv

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
