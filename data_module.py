import sqlite3
from datetime import datetime

DB_NAME = "task_manager.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')

    # Create tasks table
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    deadline TEXT,
                    priority TEXT,
                    status TEXT DEFAULT 'To Do',
                    created_at TEXT,
                    updated_at TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )''')

    conn.commit()
    conn.close()

# ---------------- User Auth ---------------- #

def register_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

# ---------------- Task Operations ---------------- #

def create_task(user_id, title, description, deadline, priority):
    now = datetime.now().isoformat()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT INTO tasks 
                 (user_id, title, description, deadline, priority, created_at, updated_at) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (user_id, title, description, deadline, priority, now, now))
    conn.commit()
    conn.close()

def get_tasks(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE user_id=?", (user_id,))
    tasks = c.fetchall()
    conn.close()
    return tasks

def update_task(task_id, title=None, description=None, deadline=None, priority=None, status=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    fields = []
    values = []

    if title:
        fields.append("title=?")
        values.append(title)
    if description:
        fields.append("description=?")
        values.append(description)
    if deadline:
        fields.append("deadline=?")
        values.append(deadline)
    if priority:
        fields.append("priority=?")
        values.append(priority)
    if status:
        fields.append("status=?")
        values.append(status)

    values.append(datetime.now().isoformat())
    values.append(task_id)

    query = f"UPDATE tasks SET {', '.join(fields)}, updated_at=? WHERE id=?"
    c.execute(query, values)
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
