import sqlite3, time

db = sqlite3.connect("data.db")
cur = db.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    name TEXT,
    username TEXT,
    role TEXT,
    backend_username TEXT,
    backend_password TEXT
)
''')
db.commit()


def register(id, name, username, role="other"):
	users = [user[0] for user in cur.execute("SELECT id FROM users").fetchall()]
	if id not in users:
		try:
			cur.execute("INSERT INTO users(id, name, username, role) VALUES(?,?,?,?)", (id, name, username, role,))
			db.commit()
		except:
			cur.execute("INSERT INTO users(id, name, username, role) VALUES(?,?,?,?)", (id, f"user_{id}", username, role,))
			db.commit()
		return
	
	try:
		cur.execute("UPDATE users SET name = ?, username = ? WHERE id = ?", (name, username, id,))
		db.commit()
	except:
		cur.execute("UPDATE users SET name = ?, username = ? WHERE id = ?", (f"user_{id}", username, id,))
		db.commit()


def get_all_data():
	return {
	    "users": cur.execute("SELECT * FROM users").fetchall(),
	}


def get_data(id):
	return {
	    "user": cur.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone(),
	}
	