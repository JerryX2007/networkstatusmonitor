import sqlite3

DATABASE = "monitor.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS monitors (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 target TEXT NOT NULL,
                 port INTEGER CHECK (port > 0 AND port < 65536) NOT NULL,
                 timeout REAL CHECK (timeout > 0) NOT NULL,
                 status TEXT,
                 latency REAL,
                 last_checked TEXT,
                 last_error TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS check_history (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 monitor_id INTEGER NOT NULL,
                 status TEXT CHECK (status IN ('online', 'offline')) NOT NULL,
                 latency REAL,
                 checked_at TEXT NOT NULL,
                 last_error TEXT,
                 FOREIGN KEY(monitor_id) REFERENCES monitors(id))''')
    conn.execute('''CREATE TABLE IF NOT EXISTS incidents (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 monitor_id INTEGER NOT NULL,
                 started_at TEXT NOT NULL,
                 resolved_at TEXT,
                 duration REAL,
                 status TEXT CHECK (status IN ('ongoing', 'resolved')) NOT NULL,
                 FOREIGN KEY(monitor_id) REFERENCES monitors(id))''')
    conn.commit()
    conn.close()