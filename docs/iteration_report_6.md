<!-----

Yay, no errors, warnings, or alerts!

Conversion time: 0.635 seconds.


Using this Markdown file:

1. Paste this output into your source file.
2. See the notes and action items below regarding this conversion run.
3. Check the rendered output (headings, lists, code blocks, tables) for proper
   formatting and use a linkchecker before you publish this page.

Conversion notes:

* Docs to Markdown version 1.0β33
* Mon Dec 05 2022 14:49:56 GMT-0800 (PST)
* Source doc: iteration_report_6
----->


**<span style="text-decoration:underline;">Project Cards</span>**

**Responsibilities:**



* Dino
    * Display a list of the user’s friends on the ‘friends’ page
    * Allow users to buy an individual card from those available in the store
* Garrett
    * Clean up the display of cards on the user inventory page (from bulleted list of info to actual card)
    * Change username and password login forms from values to placeholders
    * Display the user’s username on the home page
    * Allow a user to sell a card from their inventory for currency
* Eric
    * Make more card designs
    * Implement Mix Packs into the store table
* Karthi
    * Add Unit tests for features
    * Finish up the pack system of using pull cards to add cards to inventory
* Terasence 
    * Make trading functions to allow trades from user to user to take place

**What was completed:**



* Dino
    * Fixed adding friends app-crashing bug identified during user testing
    * Added ability to display user’s list of friends as they are added in a table on the friends page
    * Added ability to buy individual cards from the store with corresponding wallet changes (for cards that are in the ‘store’ table)
    * Added a check to methods used to buy cards which prevents users from making purchases that take their wallet balance below 0
    * Added prices to all cards through the csv file
* Garrett
    * Fixed the display of packs in the marketplace
    * Fixed the display of cards on the user inventory page (from bulleted list of info to actual card forms)
    * Changed the username and password login forms from values to placeholders
    * Added a display of the user’s username who is currently logged in on the home page
    * Added the ability for a user to sell a card from their inventory for currency that would be added to their wallet
* Eric
    * Made about 123 new card designs (a little over half of all the cards)
    * Turned the google drive links of those images into HTML - friendly source links (with the help of a little function I wrote)
    * Replaced the test_pack of 10 cards with a “mix pack” of 126 cards
    * Applied Dino’s purchase function to the pull_cards function so a pack can only be purchased if the user has 250 credits in their account and redirects the user back to the marketplace if they don’t
* Karthi
    * Fixed features that weren’t working properly
        * Inventories are now personalized to each user instead of a collective inventory for all users
        * Card packs are now correctly adding cards to the inventory
        * Individually bought cards are now correctly getting added to the inventory
        * Logout System wasn’t logging out properly due to POST instead of GET
        * Changed the pull_cards function to work as intended
    * Added all the cards to our database in the init_db function
    * Added Unit Tests for a few of the features for the website
* Terasence 
    * Started a function that will update the database when a trade is sent
    * Started a function that would update the database when a trade is confirmed

**What was not finished:**



* Karthi
    * There are still unit tests that need to be created for the rest of the features (Will be working on)
* Terasence 
    * Trade function still needs to be tested and reviewed by Mark or Evan

**Important things we learned:**



* Reach out for help when you are stuck. Both Professor Liffiton and Evan were able to help Garrett resolve a bug he was having when selling a card from a user’s inventory
* Sometimes sql keywords don’t turn the same color and google is not that helpful all the time

**Issues we ran into:**



* Dino
    * Adding entries to the transactions table will need to be revisited , this functionality was commented because it was preventing testing other more important features
* Garrett
    * When it came to the functions for selling cards from a user's inventory, at first I thought my code was working but realized there was a bug. If I wanted to sell a card from my inventory that had duplicates, it would sell all of them instead of just the one.
* Karthi
    * There is an issue with the unit tests that caused the UNIQUE constraint of the card_id in the cards table to be violated, bypassed with the help of Evan using INSERT or REPLACE into when adding all our cards to the cards database
* Terasence		
    * Update does not turn orange
    * Updating the database does not function correctly at the moment

**Adjustments to overall design:**



* Looking at bumping the amount of currency a user receives for creating an account from 500 to 1,000
* Trade function becoming fully functional

**Helpful tools/approaches:**



* Eric
    * This little function I wrote to convert google drive links to source links for the HTML (wasn’t sure whether or not to put it on github):

```

def link_converter():

    """ Takes a link and isolates the ID"""

    """ Takes a link's ID and appends to HTML friendly link"""

    """ BUG: doesnt convert the first link but I can't be bothered to fix it it's good enough"""

    with open('links.rtf', 'r') as f:

        for line in f:

            link = line.strip()

            removed_front_of_link = link[32:]

            link_split = removed_front_of_link.split('/', 1)

            id = link_split[0]

            print("https://drive.google.com/uc?export=view&id=" + id)

```



* Terasence 
    * Went to office hours and used flaskr plus plus to help with database modifications

**Plan for final 2 weeks:**



* Dino
    * Fix bugs surrounding the transaction log
    * Add a button to view the entries in the transaction log
    * Add a simple collection for users to complete in the collections tab
    * Adjust marketplace view so cards that aren’t uploaded to app are not displayed
* Eric
    * Finish designing the rest of the cards
    * Implement the other 7 mix packs
        * This will require some adjustments to the pull_cards function and possibly the store table since cards appear in multiple packs
* Garrett
    * Fix the filter by rarity code to fix the bug revolving around it (currently filtering cards by rank isn’t working correctly)
    * Change the amount of currency that a user gets from creating an account
    * Implement a way for a user to change their password
* Karthi
    * Finish up all the unit tests
    * Add features that would allow the user to get more currency for the packs (example: 5 of the same card in a pack: 200 free currency or something similar)
* Terasence	
    * Get trade functions working with friends and making sure ownership is applied properly.
    
