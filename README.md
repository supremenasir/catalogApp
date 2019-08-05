# Catalog App.

## Setting up the VM
- On git bash, first a virtual machine by typing 'vagrant up' from the Catalog folder. The pg_config.sh will also run and will install the required dependencies.
- Once the VM is installed, just type 'vagrant ssh' to login to the VM.
- Change the path to /vagrant. This will make you land in the Catalog folder.

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

