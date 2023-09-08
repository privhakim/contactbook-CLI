# contactbook-CLI

## Description

The Contact Book CLI is a command-line interface (CLI) application that allows you to manage your contacts. It provides features to create, view, search, delete, and export contacts in CSV or JSON formats.

## Features

- Create a new contact with a name, phone number, and group.
- View all contacts.
- Search for contacts by name.
- Delete a contact by ID.
- Export contacts to CSV or JSON formats.


 # Usage
 
 ## To create a new contact:


python contact_book.py create --name "John Doe" --phone "123-456-7890" --group "Friends"

## To view all contacts:

python contact_book.py view

## To search for a contact by name:

python contact_book.py search "John"

## To delete a contact by ID:

python contact_book.py delete 1
To export contacts:

## Export to CSV
python contact_book.py export csv contacts.csv

## Export to JSON
python contact_book.py export json contacts.json

# Contributing
Contributions are welcome! Please create a new branch for your changes and submit a pull request.

# License
This project is licensed under the MIT License