# Catalog App.

## Setting up the server
### Create user grader

Run Following commands
- adduser grader
- sudo usermod -aG sudo grader

### Setting up ports for SSH
- 

## How to run the application
- From the Catalog folder run the database_setup.py
- To add pre existing items, run lotsofmenu.py
- Start the server by typing 'python projectCatalog.py' from Linux shell

## Accessing the JSON API
Below are the URLs to prepare JSON of particular type.
### Listing all items
localhost:5000/catalog/JSON
### Listing a particular items
localhost:5000/catalog/<itemId>/JSON
### Listing all items in a category
localhost:5000/catalog/category/<categoryId>/JSON

