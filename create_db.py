import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the UserDetails table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS UserDetails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

print("Database and table created successfully!")
