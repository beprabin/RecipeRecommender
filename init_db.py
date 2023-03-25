import sqlite3

con = sqlite3.connect('database.db')

with open('schema.sql') as f:
    con.executescript(f.read())

cur = con.cursor()

cur.execute("INSERT INTO users (name, password,email) VALUES (?,?,?)",
            ('Ram','ram123','ram@gmail.com'))
cur.execute("INSERT INTO favourites(title, user_id) VALUES (?,?)",
            ('Thanksgiving Mac and Cheese',1))
cur.execute("INSERT INTO favourites(title, user_id) VALUES (?,?)",
            ('Apples and Oranges',1))
con.commit()
con.close()