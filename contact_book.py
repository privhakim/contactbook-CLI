import click
import os
import csv
import json
import sqlite3

# Define the database connection and cursor
conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()

# Check if the group_id column already exists in the contacts table
cursor.execute("PRAGMA table_info(contacts)")
columns = cursor.fetchall()
column_names = [column[1] for column in columns]
if 'group_id' not in column_names:
    # Add the group_id column to the contacts table if it doesn't exist
    cursor.execute("ALTER TABLE contacts ADD COLUMN group_id INTEGER")
    conn.commit()

@click.group()
def cli():
    pass

@cli.command()
@click.option('--name', prompt='Name', help='Name of the contact', required=True)
@click.option('--phone', prompt='Phone', help='Phone number of the contact')
@click.option('--group', prompt='Group', help='Group name for the contact')
def create(name, phone, group):
    """Create a new contact."""    
    
    cursor.execute("INSERT OR IGNORE INTO groups (name) VALUES (?)", (group,))
    conn.commit()

    
    cursor.execute("SELECT id FROM groups WHERE name=?", (group,))
    group_id = cursor.fetchone()[0]

    
    cursor.execute("INSERT INTO contacts (name, phone, group_id) VALUES (?, ?, ?)", (name, phone, group_id))
    conn.commit()

    click.echo('Contact created successfully!')

@cli.command()
def view():
    """View all contacts."""
    cursor.execute("SELECT contacts.id, contacts.name, contacts.phone, groups.name FROM contacts JOIN groups ON contacts.group_id = groups.id")
    contacts = cursor.fetchall()

    if contacts:
        for contact in contacts:
            click.echo(f'ID: {contact[0]}, Name: {contact[1]}, Phone: {contact[2]}, Group: {contact[3]}')
    else:
        click.echo('No contacts found.')

@cli.command()
@click.argument('name')
def search(name):
    """Search for a contact by name."""
    cursor.execute("SELECT contacts.id, contacts.name, contacts.phone, groups.name FROM contacts JOIN groups ON contacts.group_id = groups.id WHERE contacts.name LIKE ?", (f"%{name}%",))
    contacts = cursor.fetchall()

    if contacts:
        for contact in contacts:
            click.echo(f'ID: {contact[0]}, Name: {contact[1]}, Phone: {contact[2]}, Group: {contact[3]}')
    else:
        click.echo('No matching contacts found.')

@cli.command()
@click.argument('id', type=int)
def delete(id):
    """Delete a contact by ID."""
    cursor.execute("DELETE FROM contacts WHERE id = ?", (id,))
    conn.commit()

    click.echo('Contact deleted successfully!')

@cli.command()
@click.argument('format', type=click.Choice(['csv', 'json']))
@click.argument('filename', type=click.Path())
def export(format, filename):
    """Export contacts to CSV or JSON."""
    cursor.execute("SELECT contacts.id, contacts.name, contacts.phone, groups.name FROM contacts JOIN groups ON contacts.group_id = groups.id")
    contacts = cursor.fetchall()

    if format == 'csv':
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Name', 'Phone', 'Group'])
            for contact in contacts:
                writer.writerow([contact[0], contact[1], contact[2], contact[3]])
    elif format == 'json':
        contact_list = [{'ID': contact[0], 'Name': contact[1], 'Phone': contact[2], 'Group': contact[3]} for contact in contacts]
        with open(filename, 'w') as file:
            json.dump(contact_list, file, indent=4)

    click.echo(f'Contacts exported to {filename} in {format} format.')

if __name__ == '__main__':
    cli()
