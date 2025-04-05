import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
""")

# Add a default user
cursor.execute("INSERT OR REPLACE INTO users (username, password) VALUES (?, ?)", ("testuser123", "123456"))

conn.commit()
conn.close()

print("✅ Database initialized with test user.")
