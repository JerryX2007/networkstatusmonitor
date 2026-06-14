import sqlite3

DATABASE = "monitor.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS monitors (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 target TEXT,
                 port INTEGER,
                 timeout REAL,
                 status TEXT,
                 latency REAL,
                 last_checked TEXT,
                 last_error TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS check_history (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 monitor_id INTEGER,
                 status TEXT,
                 latency REAL,
                 checked_at TEXT,
                 last_error TEXT,
                 FOREIGN KEY(monitor_id) REFERENCES monitors(id))''')
    conn.execute('''CREATE TABLE IF NOT EXISTS incidents (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 monitor_id INTEGER,
                 started_at TEXT,
                 resolved_at TEXT,
                 duration REAL,
                 status TEXT,
                 FOREIGN KEY(monitor_id) REFERENCES monitors(id))''')
    conn.commit()
    conn.close()