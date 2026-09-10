Feature: CoffeeMakerFeature

In this feature, we are going to test the user stories and use cases for the CoffeeMaker
Example.  We have provided a CoffeeMakerMain.java file that you can use to examine the 
modal behavior in the coffee maker and issue UI commands to use it, so that we can 
adequately test the user stories.

Hints: to catch the mistakes, you might need to add out of range cases for 
recipes and amounts of ingredients.  Also, be sure to check machine state
after running the user story:
  - Are the amounts of ingredients correct?
  - Is the system in the right mode?
  - Is the status what you expect?
  - Is the change produced correct?
  - etc.

Scenario: Waiting State
      Priority: 1 Story Points: 2
      If the Coffee Maker is not in use it waits for user input. There are six different 
      options of user input: 1) add recipe, 2) delete a recipe, 3) edit a recipe, 
      4) add inventory, 5) check inventory, and 6) purchase beverage.
      
      For this scenario, what we will do is try each of the six user inputs and make sure 
      that the coffee maker ends up in the appropriate mode.  This would be a good place
      for a scenario outline with a table that described user inputs and expected final states.
      
      You might also want to try a couple of exceptional values to see what the 
      Coffee Maker does.
      
   Given a default recipe book
   When I select every service from the waiting state
   Then each service opens its expected mode
   
Scenario: Add a Recipe
      Priority: 1 Story Points: 2

      Only three recipes may be added to the CoffeeMaker. A recipe consists of a name, 
      price, units of coffee, units of milk, units of sugar, and units of chocolate. 
      Each recipe name must be unique in the recipe list. Price must be handled as an 
      integer. A status message is printed to specify if the recipe was successfully 
      added or not. Upon completion, the CoffeeMaker is returned to the waiting state.   
      
      For this scenario, you should try to add a recipe to the recipe book, and check to
      see whether the coffee maker returns to the Waiting state.  
      
   Given an empty recipe book
   When I add a valid recipe through the interface
   Then the recipe is stored and the interface waits
   
Scenario: Delete a Recipe
      Priority: 2 Story Points: 1

      A recipe may be deleted from the CoffeeMaker if it exists in the list of recipes in the
      CoffeeMaker. The recipes are listed by their name. Upon completion, a status message is
      printed and the Coffee Maker is returned to the waiting state.  

   Given a default recipe book
   When I delete an existing recipe and try to delete an empty slot
   Then deletion reports the correct outcomes
   

Scenario: Edit a Recipe
      Priority: 2 Story Points: 1

      A recipe may be edited in the CoffeeMaker if it exists in the list of recipes in the
      CoffeeMaker. The recipes are listed by their name. After selecting a recipe to edit, the user
      will then enter the new recipe information. A recipe name may not be changed. Upon
      completion, a status message is printed and the Coffee Maker is returned to the waiting
      state.  

   Given a default recipe book
   When I edit an existing recipe and select an invalid recipe
   Then editing preserves the recipe name and rejects the invalid selection
   
Scenario: Add Inventory
      Priority: 1 Story Points: 2

      Inventory may be added to the machine at any time from the main menu, and is added to
      the current inventory in the CoffeeMaker. The types of inventory in the CoffeeMaker are
      coffee, milk, sugar, and chocolate. The inventory is measured in integer units. Inventory
      may only be removed from the CoffeeMaker by purchasing a beverage. Upon completion, a
      status message is printed and the CoffeeMaker is returned to the waiting state.   
      
   Given a default recipe book
   When I add valid inventory and request the inventory report
   Then the inventory report contains the added amounts
   
Scenario: Check Inventory 
      Priority: 2 Story Points: 1

      Inventory may be checked at any time from the main menu. The units of each item in the
      inventory are displayed. Upon completion, the Coffee Maker is returned to the waiting state.  
      
   Given a default recipe book
   When I request the inventory report
   Then the inventory report contains the added amounts
   
Scenario: Purchase Beverage
      Priority: 1 Story Points: 2

      The user selects a beverage and inserts an amount of money. The money must be an
      integer. If the beverage is in the RecipeBook and the user paid enough money the
      beverage will be dispensed and any change will be returned. The user will not be able to
      purchase a beverage if they do not deposit enough money into the CoffeeMaker. A user's
      money will be returned if there is not enough inventory to make the beverage. Upon
      completion, the Coffee Maker displays a message about the purchase status and is
      returned to the main menu.  
      
   Given a default recipe book
   When I buy a recipe with enough money and then with insufficient money
   Then the purchase returns change only for the successful purchase


Scenario: Domain validation and recipe book boundaries
   Given an empty recipe book
   When I exercise recipe, inventory, and recipe book boundary cases
   Then valid domain state is retained and invalid values are rejected

Scenario: Interface errors and alternate purchase flows
   Given an empty recipe book
   When I exercise interface error handling and alternate purchase flows
   Then the interface returns to a consistent waiting state

Scenario: Remaining interface and validation branches
   Given an empty recipe book
   When I exercise the remaining interface and validation branches
   Then all alternate flows preserve a valid state