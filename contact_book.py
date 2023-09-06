import click
import os
import csv
import json
import sqlite3

@click.group()
def cli():
    pass

@cli.command()
@click.option('--name', prompt='Name', help='Name of the contact', required=True)
@click.option('--phone', prompt='Phone', help='Phone number of the contact')
@click.option('--group', prompt='Group', help='Group name for the contact')
def create(name, phone, group):
    """Create a new contact."""
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()

    
    cursor.execute("INSERT OR IGNORE INTO groups (name) VALUES (?)", (group,))
    conn.commit()

    
    cursor.execute("SELECT id FROM groups WHERE name=?", (group,))
    group_id = cursor.fetchone()[0]

    
    cursor.execute("INSERT INTO contacts (name, phone, group_id) VALUES (?, ?, ?)", (name, phone, group_id))
    conn.commit()

    conn.close()
    click.echo('Contact created successfully!')

@cli.command()
def view():
    """View all contacts."""
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()

    cursor.execute("SELECT contacts.id, contacts.name, contacts.phone, groups.name FROM contacts JOIN groups ON contacts.group_id = groups.id")
    contacts = cursor.fetchall()

    if contacts:
        for contact in contacts:
            click.echo(f'ID: {contact[0]}, Name: {contact[1]}, Phone: {contact[2]}, Group: {contact[3]}')
    else:
        click.echo('No contacts found.')

    conn.close()

@cli.command()
@click.argument('name')
def search(name):
    """Search for a contact by name."""
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()

    cursor.execute("SELECT contacts.id, contacts.name, contacts.phone, groups.name FROM contacts JOIN groups ON contacts.group_id = groups.id WHERE contacts.name LIKE ?", (f"%{name}%",))
    contacts = cursor.fetchall()

    if contacts:
        for contact in contacts:
            click.echo(f'ID: {contact[0]}, Name: {contact[1]}, Phone: {contact[2]}, Group: {contact[3]}')
    else:
        click.echo('No matching contacts found.')

    conn.close()    