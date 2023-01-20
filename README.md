This is the first assignment for ICCS372: Software Engineering
I utilized Django to develop my Vending Machine management system. To run it, enter the repository that contains the manage.py file via the terminal. Once here, run "python manage.py runserver" and access the server by utilizing the url "http:127.0.0.0:8000". Functionality goes as follows:

----------------------Home-----------------------------
The Home Page contains a table that presents all of the existing Vending Machines. The Vending Machine names are clickable links that upon clicking forwards you to the Vending Machine's page. 
Below this table, is a table that shows the current stock of all codes, which includes total stock (which includes those inside of vending machines), and available stock (capacity to be added to Vending Machines). This table has an edit button below that redirects to the stock page for stock editing

----------------------Create VM-----------------------------
Contains a simple form that has asks for where Vending Machine's location will be. If there's no Vending Machine at this location, the vending machine will be created.

----------------------Stock-----------------------------
The stock page shows a table like the one appearing in our home page. It additionally has the capabilitis of creating new snacks, and updating stock details.

----------------------Vending Machine Page-----------------------------
Vending Machines can be reached by the home page, where all existing vending machines are displayed and forward to their management pages. Within the vending machine page, we can add snacks to the vending machine's individual stock, which also updates the database in the background. 
Each page display's the vending machines current stock in a table, with a purchase button that allows for the purchase of items.  
In addition, we have a stock editing form, in case we may want to remove items from the vending machine.
Finally we have the delete Vending Machine button, and a table with the availability of stock, so we can add and edit stock easily.

