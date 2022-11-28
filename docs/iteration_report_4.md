**<span style="text-decoration:underline;">Digital Trading Cards</span>**


**Responsibilities:**






* Eric
    * Help with getting users to “own” cards, add more cards to the database, and make simple designs for those cards
* Dino
    * Implement a friends list (table) in the database and add a way for users to add others to the friends list via input form
* Garrett
    * Tasked with implementing a currency system to our application that will allow users to buy packs or cards listed on the marketplace and or sell cards
    * Also helped create some of the new cards as well along with Eric
* Karthi
    * Help with getting users to own cards
    * **Later changed to adding a system where bought cards from the marketplace would be added to the inventory.**
* Terasence 
    * Design the Trading related pages and start developing a system for trading.


**What was completed:**






* Eric
    * Made 204 new cards (4 new themes) with Garrett’s help
    * Made 7 “Mix Packs” that randomly picks 126 cards (50 of rank 1, 37 of rank 2, 25 of rank 3, 12 of rank 4, and 2 of rank 5) with the intention that these will be the packs people can buy and draw from
    * Drew up some simple (and possibly final) designs for a few cards with the intention to test displaying cards on the web app
    * All this was done on Google Sheets which is shared with everyone in the group and with Mark
* Dino
    * Created friends table in the database 
    * Implemented adding friends by writing the add_friends method, and adding a functional text input to the friends page to add friend usernames
    * Altered login method to use sesion[] to log which user is using the app
    * Fixed flash messages bug which prevented flash messages from being displayed
    * Added a logout button to the home screen and implemented logout functionality with the logout method
    * Changed password input to password type so dot characters are displayed in the input field
* Garrett
    * Added a new column to the user table that will store the user’s balance (this is called wallet_balance and has a default value)
    * Began writing code in both app.py and home.html to display the user balance on the page
    * Talking with Mark - created a new table called transactions that will be a log of transactions for users
    * Added a bunch of new cards to our spreadsheet along with Eric
    * Changed login form fields from values to placeholders
* Karthi
    * Added a way for users to see all cards in a simple way for testing purposes
    * Added a add_cards function to app.py that adds cards when buy button is clicked on the marketplace
    * Added a way for users to buy every card in the marketplace (Will be expanded on when currency is finished)
* Terasence
    * Created the trade page,trade request page, and trade confirmation page.
    * Added images and buttons to the UI that tells the user how to trade.
    * Added links to some of the main buttons to take you to the respective page.


**What was not finished:**






* Eric
    * Did more than anticipated with the cards, but did not end up writing much of any code.
    * Was supposed to help Karthi with ownership of cards, but only got as far as redesigning the collection table with Dino’s help.
* Garrett
    * Code in both app.py and html definitely needs some more work during the next iteration
    * Plan to continue working on the currency system during the iteration over the break
    * My branch hasn’t been merged yet since it is still a work in progress
* Karthi
    * Packs still need to be worked on in a way so that packs have random cards from different sections of cards
    * Currency system for each card
* Terasence
    * Buttons do not work yet for selecting cards.
    * A trading system has not been finished.
    * The images of cards are not connected into the trade pages 


**Important things we learned:**






* Eric
    * Spreadsheets are a very useful tool for managing and manipulating data.
* Karthi
    * Testing code is extremely important and needs to be done first to make sure that the code is working while properly checking through any errors that happen. (Testing can’t be the last thing that is done.)
* Terasence
    * Designing a page on paper can save a lot of time because jotting it down will bring up questions and ideas that you will more than likely not think of when freestyling instead of planning


**Issues we ran into:**






* Dino
    * Git setup seems to cause problems in some way every week - adding changes to the repository never goes smoothly
* Garrett
    * Had an extremely busy tail end of the week and began to feel under the weather over the weekend
    * A little progress was made but not a ton this week
* Eric
    * Given a lack of experience with Google Sheets or Excel, it was difficult to create the mixed packs and ended up getting stumped. This hindered progress for longer than necessary.
* Karthi
    * Difference between GET and POST and how they affect the routes when a form is called
    * Difference between request.args and request.form (request.args is for GET methods, while request.form is for POST methods)
* Terasence
    * Adding buttons can affect the spacing of containers,rows and columns on the screen.
    * Some errors came from incorrectly linking pages to one another. 
    * Small syntax mistakes that were fixed from indenting and checking for brackets to be closed.


**Adjustments to overall design:**






* Collection table now only takes user_id and card_id. Both are foreign keys referencing the user table and the cards table respectively. This requires changes to the pull_cards() function.
* Decided to add a SQL table that will track all of the transactions (advice given from Mark on how to implement this).
* Adding the trade pages and using images with buttons to the UI so the user can easily understand how to trade.


**Helpful tools/approaches:**






* GIT cookbook (refreshing memory on how to work with branches)
* Mark’s office hours


**Plan for next iteration:**






* Garrett plans to continue working on where he left off with his currency system over the break. He plans to continue writing the Python and HTML code to display the user’s wallet on a page. He also plans on looking at working more with the transactions table as we start to implement buying and selling cards within our application.
* Karthi plans to add a way for users to buy packs and the randomization factor of the packs. (Might need to add type attribute to cards to differentiate between different packs)
* Terasence plans to work on a system of trading cards
* Eric plans on getting card visuals to appear on the website and starting on getting the store page running with the mix packs.
* Dino plans on setting up the transaction logs with possible help from Garrett for management of user purchases.


**Plan for future iterations:**






* Currency system and the way it interacts with the marketplace and user balance need to be fleshed out.
* Trade system that will allow users to trade cards with other users
* A lot of images that represent the cards