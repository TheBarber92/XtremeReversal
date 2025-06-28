import sqlite3
import hashlib

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, password TEXT, uploads INTEGER)")
conn.commit()

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def register_user(user_id, password):
    try:
        cursor.execute("INSERT INTO users (id, password, uploads) VALUES (?, ?, ?)", (user_id, hash_pw(password), 0))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(user_id, password):
    cursor.execute("SELECT password FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    return row and row[0] == hash_pw(password)

def check_upload_limit(user_id):
    cursor.execute("SELECT uploads FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    return row and row[0] < 2

def increment_uploads(user_id):
    cursor.execute("UPDATE users SET uploads = uploads + 1 WHERE id=?", (user_id,))
    conn.commit()