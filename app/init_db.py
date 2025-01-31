import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

cursor.executemany("INSERT INTO users (user_name, password) VALUES (?, ?)", [
    ('user1', 'password1'),
    ('user2', 'password2'),
    ('user3', 'password3')
])

conn.commit()
conn.close()

print("データベースを初期化しました。")
