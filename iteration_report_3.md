**<span style="text-decoration:underline;">Digital Trading Cards</span>**

**Responsibilities:**



* Garrett 
    * Worked on adding functionality to buttons within our pages. Now, the home buttons that are present within some of the pages will bring you back to the home page of our web application. 
    * Garrett also worked on adding more Bootstrap code to make our pages look cleaner and more user friendly. 
    * Within the your_inventory page, he added a way to filter a user's owned cards by rarity. 
    * Lastly, he started to work on a new app route called friends_inventory that will be tied to the friends page and will allow a user to view a friends card inventory. In the future, we plan on also adding the ability to trade with a friend as well.
* Dino 
    * Finished user authentication by fixing a bunch of bugs surrounding incorrect usernames/passwords and users attempting to use duplicate usernames/emails. 
    * Instead of crashing the application the user is redirected to the input fields so they can try again. 
* Eric 
    * Worked on a method to randomly pick cards out of the database with the intent to move these cards to a user’s personal collection.
* Karthi
    * Worked on bootstrapping the your_inventory.html page
    * Added a way to filter cards by rank for when the user checks the cards
* Terasence
    * Intended to implement a card management system that applies cards acquired by users to an individual's inventory. After this was completed a trading card system was next to be implemented.

**What was completed:**



* Garrett
    * Was able to successfully add functionality to the home and view collection buttons within our applications pages. 
    * He was also able to continue adding Bootstrap code to make our pages look cleaner and more user friendly as well. This will be an ongoing task as more functionality and new things continue to get added to our application. 
    * Within the your_inventory page, a way to filter user-owned cards by rarity was completed. 
* Dino 
    * Successfully cleaned up all known bugs in user authentication to force users to create unique accounts that allow them to log in securely. 
* Eric 
    * Made a first iteration of the random card picker called pull_cards(). It successfully picks 5 cards and inserts them into the collection table.
* Karthi
    * Implemented bootstrap into your_inventory.html
    * Added a way to filter cards by rank
    * Fixed a bug where every card’s rank would be shown instead of just 1-5

**What was not finished:**



* Garrett finished what he planned on for this iteration so he also started a new app route called friends_inventory that will be tied to the friends page and that will allow a user to view a friends card inventory. This is still in the early stages of development and will be continued as we add friends to our application.
* Although the pull_cards() method is mostly finished, getting an individual user’s table still needs to be worked on. Additionally, the method does not take into account future packs of cards or combinations of packs of cards that we might intend to pull from when a user purchases different packs.
* A system that adds cards to an individual inventory and a trade system to allow users to trade cards. A use of joins that trade from table to table in sql was proposed but not developed by Terasence.

**Important things we learned:**



* Try to get help on fixing issues earlier and communicate with the team on what you are struggling with, instead of just mulling it over for days with no results.
* Important to have a more concrete and explicit planning for tasks instead of a looser task load for each individual person

**Issues we ran into:**



* A bug where every cards’ rank would be shown when filtered.
* A problem with using git and committing the local changes in the right way into GitHub.

**	**

**Adjustments to overall design:**



* During this iteration, we added a lot of bootstrap to the overall website, which made the website’s overall design much better to look at. As we move on, this would need to be constantly updated.

**Helpful tools/approaches:**



* End of week meeting, this was really helpful to figure out our game plan for the next week. This also allowed us to brainstorm any issues we had during the week or any issues we might run into over the next few iterations.
* StackOverflow was very useful when figuring out what to do to fix some of the issues Karthi had during the committing time in git bash.
* Terasence will meet with Mark every office hours period available and use at least 10 min to look over iteration status and go over the current report.

**Plan for next iteration:**



* With the pull_cards method mostly finished, we can work towards getting a more definitive method of getting users to “own” cards. Using form requests we can also work towards displaying these cards. Along with working on individual user collections, it might also be useful to work on simple designs for the cards to be displayed in our application. This is what Eric and Karthi will focus on.
* Dino will focus on implementing a ‘friends list’: being able to enter a username and add the corresponding user, provided the username is valid. 
* Garrett will focus on creating a currency system that will allow users to buy packs or cards listed on the marketplace. Garrett also plans to help work on adding more cards into our SQL database. Currently, we have 52 cards and as a group we feel that we still need more cards.
* Terasence will create a system where users can trade cards. This system will allow users to search up a username that pulls the desired user's card inventory. After seeing the user's inventory there will be a trade button that takes you to a screen where you can submit the cards you want to offer and the cards you would like to receive. Then the trade gets sent to the other user's “pending trades” page that shows trades that were offered to him. This pending trade screen will be able to be accessed at any time in the same place on all pages and is a button that will look like “Pending trades (2)” where the number in parenthesis is the amount of trades pending.

**Plan for future iterations:**



* Implement a way for users to change their password
* Allow users to buy and sell cards in the marketplace
* Allow users to trade cards with their friends
* Implement currency-based rewards for completing collections
* Ability for friends to message each other

