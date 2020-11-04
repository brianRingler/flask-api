import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# to auto increment the id must use full word INTEGER
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

query = "SELECT * FROM users"
rows = cursor.execute(query)
for row in rows:
    print(row)
    
connection.commit()

connection.close()
