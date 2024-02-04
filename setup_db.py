import sqlite3


db_file = 'message_board.db'

# Connect to SQLite database (creates a new one if not exists)
conn = sqlite3.connect(db_file)

# Create Users Table
conn.execute('''
    CREATE TABLE IF NOT EXISTS User (
        user_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        password TEXT NOT NULL,
        ip TEXT,
        port INTEGER,
        CONSTRAINT unique_name_password UNIQUE (name, password)
    )
''')

# Create Groups Table
conn.execute('''
    CREATE TABLE IF NOT EXISTS Chat (
        chat_id INTEGER PRIMARY KEY,
        chat_name TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Create Group_Members Table
conn.execute('''
    CREATE TABLE IF NOT EXISTS Chat_Members (
        chat_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (chat_id) REFERENCES Chat(chat_id),
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        PRIMARY KEY (chat_id, user_id)
    )
''')

# Create Messages Table
conn.execute('''
    CREATE TABLE IF NOT EXISTS Message (
        message_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        chat_id INTEGER NOT NULL,
        encryption INTEGER,
        content TEXT NOT NULL,
        message_date TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (chat_id) REFERENCES Chat(chat_id)
    )
''')


conn.execute('''
    CREATE TABLE IF NOT EXISTS Listener (
        listener_id INTEGER PRIMARY KEY,
        chat_id INTEGER,
        ip TEXT NOT NULL,
        port INTEGER NOT NULL,
        FOREIGN KEY (chat_id) REFERENCES Chat(chat_id)
    )
''')

# Create Raw Table
conn.execute('''
    CREATE TABLE IF NOT EXISTS Raw (
        raw_id INTEGER PRIMARY KEY,
        time TEXT DEFAULT CURRENT_TIMESTAMP,
        ip TEXT NOT NULL,
        port INTEGER NOT NULL,
        data TEXT NOT NULL
    )
''')

# Commit changes
conn.commit()

result = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")

# Fetch all rows
tables = result.fetchall()

# Extract table names from the result
table_names = [table[0] for table in tables]

# Print the list of tables
print("List of tables in the database:")
for table_name in table_names:
    print("......" + table_name)

print("Tables created successfully.")

conn.execute("INSERT INTO User (name, password) VALUES ('x', 'x')")
conn.execute("INSERT INTO Chat (chat_name, password) VALUES ('x', 'x')")

# Commit changes and close connection
conn.commit()

conn.close()

print("Connections closed.")
