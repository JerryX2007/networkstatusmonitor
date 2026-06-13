from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import socket
import time

app = FastAPI()

class Monitor(BaseModel):
    name: str
    target: str
    port: int = 80
    timeout: float = 3.0

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
    conn.commit()
    conn.close()

init_db()

def find_monitor(monitor_id: int):
    conn = get_db()
    cursor = conn.execute("SELECT * FROM monitors WHERE id = ?", (monitor_id,))
    monitor = cursor.fetchone()
    conn.close()
    if monitor:
        return dict(monitor)
    return None


@app.post("/monitors")
def add_monitor(monitor: Monitor):
    conn = get_db()
    cursor = conn.execute(
        """
        INSERT INTO monitors
        (name, target, port, timeout, status, latency, last_checked, last_error)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (monitor.name, monitor.target, monitor.port, monitor.timeout, None, None, None, None)
    )
    conn.commit()
    monitor_id = cursor.lastrowid

    row = conn.execute("SELECT * FROM monitors WHERE id = ?", (monitor_id,)).fetchone()
    conn.close()
    return dict(row)

@app.get("/monitors")
def get_monitors():
    conn = get_db()
    cursor = conn.execute("SELECT * FROM monitors")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/monitors/{monitor_id}")
def read_monitor(monitor_id: int):
    monitor = find_monitor(monitor_id)
    if monitor:
        return monitor
    raise HTTPException(status_code=404, detail="Monitor not found")

@app.post("/monitors/{monitor_id}/check")
def check_monitor(monitor_id: int): 
    monitor = find_monitor(monitor_id)
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(monitor["timeout"])
    start_time = time.perf_counter()
    try:
        sock.connect((monitor["target"], monitor["port"]))
        end_time = time.perf_counter()
        latency = (end_time - start_time) * 1000
        latency = round(latency, 2)
        monitor["status"] = "online"
        monitor["latency"] = latency
        monitor["last_error"] = None
    except socket.timeout:
        monitor["status"] = "offline"
        monitor["latency"] = None
        monitor["last_error"] = "Connection timed out"
    except socket.error as e:
        monitor["status"] = "offline"
        monitor["latency"] = None
        monitor["last_error"] = str(e)
    finally:
        monitor["last_checked"] = time.strftime("%Y-%m-%d %H:%M:%S")
        conn = get_db()
        conn.execute(
            """
            UPDATE monitors
            SET status = ?, latency = ?, last_checked = ?, last_error = ?
            WHERE id = ?
            """,
            (monitor["status"], monitor["latency"], monitor["last_checked"], monitor["last_error"], monitor_id)
        )
        cursor = conn.execute(
            """
            INSERT INTO check_history
            (monitor_id, status, latency, checked_at, last_error)
            VALUES (?, ?, ?, ?, ?)
            """,
            (monitor_id, monitor["status"], monitor["latency"], monitor["last_checked"], monitor["last_error"])
        )
        conn.commit()
        recent = cursor.lastrowid
        row = conn.execute("SELECT * FROM check_history WHERE id = ?", (recent,)).fetchone()
        conn.close()
        sock.close()
    return dict(row)

@app.get("/monitors/{monitor_id}/history")
def get_monitor_history(monitor_id: int):
    monitor = find_monitor(monitor_id)
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")
    conn = get_db()
    cursor = conn.execute("SELECT * FROM check_history WHERE monitor_id = ?", (monitor_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.delete("/monitors/{monitor_id}")
def delete_monitor(monitor_id: int):
    monitor = find_monitor(monitor_id)
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")
    conn = get_db()
    conn.execute("DELETE FROM monitors WHERE id = ?", (monitor_id,))
    conn.commit()
    conn.close()
    return {"message": "Monitor deleted"}

@app.put("/monitors/{monitor_id}")
def update_monitor(monitor_id: int, monitor: Monitor):
    m = find_monitor(monitor_id)
    if not m:
        raise HTTPException(status_code=404, detail="Monitor not found")
    conn = get_db()
    conn.execute(
        """
        UPDATE monitors
        SET name = ?, target = ?, port = ?, timeout = ?
        WHERE id = ?
        """,
        (monitor.name, monitor.target, monitor.port, monitor.timeout, monitor_id)
    )
    row = conn.execute("SELECT * FROM monitors WHERE id = ?", (monitor_id,)).fetchone()
    conn.commit()
    conn.close()
    return dict(row)