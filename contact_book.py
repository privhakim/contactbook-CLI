import sqlite3
db_file = "contacts.db"

def initialize_database():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.excute('''
        CREATE TABLE IF NOT EXISTS contacts(
                  id INTEGER PRIMARY KEY,
                  name TEXT,
                  phone TEXT,
                  )
    ''')

    conn.commit()
    conn.close()

initialize_database()