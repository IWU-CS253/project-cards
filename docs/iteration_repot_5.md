**<span style="text-decoration:underline;">Digital Trading Cards</span>**

**Responsibilities:**



* Garrett
    * Garrett continued where he left off with the currency system. There is now officially a new column attribute called wallet_balance in the user table that will be used as the user’s wallet. Garrett also continued to write Python and HTML code this iteration to display the user’s balance on the home page.
* Dino
    * Set up transaction log to track activity on the site, add functionality for card purchases
* Eric
    * Get cards to show up on the website and continue making packs/images for the cards.
* Terasence 
    * Clean up the trading pages and start making a trading function to allow cards to be traded from user to user
* Karthi
    * Add a pack system where users can buy a pack that would add random cards to the user’s collection, based on the previously written pull_cards() by Eric

**What was completed:**



* Garrett
    * As mentioned above, Garrett officially completed adding a new column attribute called wallet_balance in the user table that will be used to display a user’s wallet. Garrett also was able to write out a Python function called wallet_balance that includes code that works to display the wallet. Garrett also wrote out a new transaction table that will be used as a log to track user’s transactions. 
* Dino
    * Created a table to log transactions as they occur on the app, created a purchase() method to handle pack and card purchases, also created a buy_cards() method which calls purchase() in order to make the correct adjustments to user inventory and wallet when buying a card. 
* Eric
    * Made a new page where, after a pack is purchased, the cards the user pulls are shown.
    * Redesigned the store table to hold images as an attribute.
* Terasence 
    * Trading pages work and are properly linked together and organized
* Karthi
    * Changed all of the adding cards to the collection because they weren’t working as intended (bug fix)
    * Changed the login system a bit to fix a bug that didn’t record session’s user_id (bug fix)
    * Added packs in the marketplace that would use pull_cards() that was previously written. 
    * Added a new page pack_contents that shows all the cards that were gotten in the pack (Commented out because it can’t be tested until the next week)
* Garrett / Karthi
    * Changed the create user system to have auto incrementing primary key(user_id) instead of it being created as a NULL (bug)

**What was not finished:**



* Garrett
    * Garrett was having trouble actually displaying the user’s balance in their wallet. Garrett has been in contact with both Mark and Evan about the problem and Garrett was actually able to display a user’s wallet balance on the home page. Evan and Karthi helped him find that our user_id was printing NULL, so we just had to update it to be auto incrementing in the users table. 
* Eric
    * Ownership of cards is still not fully implemented. When cards are pulled, they are moved to the collection table, but with a temporary user_id of 1.
* Terasence	
    * Trade function was more difficult than expected. Ideas and potential plans were developed but I lacked the ability to implement them without more experienced help.

**Important things we learned:**



* Garrett
    * Reach out for help if you get stuck on a bug
* Terasence 
    * Take time to make sure all indentation and bootstrap is in the right places to avoid confusion. 
    * Use other working code to reference structure to fix errors.
    * Check all brackets individually when checking syntax

**Issues we ran into:**



* Garrett
    * As mentioned above, Garrett ran into issues with getting the user balance to display the user’s wallet balance. Currently, the words wallet balance are displayed on the home page and a default value (500) is shown thanks to help from Evan and Karthi. 500 is the default value as this amount is the amount given to a user who creates an account.
* Dino
    * Was hung up on a dumb error for a while which was caused by forgetting to call db.execute in front of an sql query
* Karthi
    * Ran into issues with getting the current user from the app and comparing it to the users table
    * Was not able to work on the packs too much due to the new collection table and the way cards were being added to the collection and the need for it to be fixed
* Terasence	
    * Struggled with getting bootstrap to be properly implemented due to indentation errors because sometimes it can work others it will fail
    * Struggled with developing a trading function 

**Adjustments to overall design:**



* The store table now no longer has the name of the card as an attribute. Instead it has the image of the card and the pack it’s from (this will be multivalued as cards can be from multiple ‘Mix Packs’).
* Pull_cards() pulls from the store table now, and not the cards table.
* Trading pages are functional and now the site has a place for trades to take place.
* Changed the way cards are added to the collection table 

**Helpful tools/approaches:**



* Garrett
    * Reaching out to group members for help is very beneficial. If they can’t help with the issue, then reach out to Mark or Evan to see if they can help provide helpful insight on potential fixes for bugs.
* Terasence	
    * Taking as many steps back as possible to fully understand issues that arrive and slowly going back to the previous point.

**Plan for next iteration:**



* Garrett
    * Garrett was able to fix the bug regarding the wallet balance not being printed
    * He now plans on updating the pull_cards.html page a bit as well as looking into writing a sell() method that will be used if a user sells a card
* Dino
    * Display a list of the user’s friends on the ‘friends’ page
    * Allow users to buy an individual card from those available in the store
* Eric
    * Make more card designs
    * Implement the Mix Packs into the store table
* Karthi
    * Complete Unit Tests for the features
    * Finish Packs using the new pull_cards that was added this iteration
* Terasence
    * Meet with Mark/Evan and develop a trading function	

**Plan for future iterations:**



* Finalize ownership of cards by automatically assigning a user_id to new users. 
* Continue to work with currency (add prices to cards and packs in the marketplace) and be able to add or lose currency based on if they are selling or buying cards.
* Finalize transfer of ownership of cards through trading and alerting the users of finalized trades.
