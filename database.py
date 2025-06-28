import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            upload_count INTEGER DEFAULT 0,
            paid INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result

def increment_upload(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    if result:
        c.execute("UPDATE users SET upload_count = upload_count + 1 WHERE user_id = ?", (user_id,))
    else:
        c.execute("INSERT INTO users (user_id, upload_count, paid) VALUES (?, ?, ?)", (user_id, 1, 0))
    conn.commit()
    conn.close()

def has_access(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT upload_count, paid FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        upload_count, paid = row
        return paid == 1 or upload_count < 2
    return True