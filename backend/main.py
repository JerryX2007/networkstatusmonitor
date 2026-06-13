from fastapi import FastAPI
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

monitors = []
check_history = []

def find_monitor(monitor_id: int):
    for monitor in monitors:
        if monitor["id"] == monitor_id:
            return monitor
    return None

@app.post("/monitors")
def add_monitor(monitor: Monitor):
    new_monitor = {
        "id": len(monitors) + 1,
        "name": monitor.name,
        "target": monitor.target,
        "port": monitor.port,
        "timeout": monitor.timeout,
        "status": None,
        "latency": None,
        "last_checked": None,
        "last_error": None
    }
    monitors.append(new_monitor)
    return new_monitor

@app.get("/monitors")
def get_monitors():
    return monitors

@app.get("/monitors/{monitor_id}")
def read_monitor(monitor_id: int):
    monitor = find_monitor(monitor_id)
    if monitor:
        return monitor
    return {"error": "Monitor not found"}

@app.get("/monitors/{monitor_id}/check")
def check_monitor(monitor_id: int):
    monitor = find_monitor(monitor_id)
    if not monitor:
        return {"error": "Monitor not found"}
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
        check_history.append({
            "monitor_id": monitor_id,
            "status": monitor["status"],
            "latency": monitor["latency"],
            "checked_at": monitor["last_checked"],
            "last_error": monitor["last_error"]
        })
        sock.close()
    return check_history[-1]

@app.get("/monitors/{monitor_id}/history")
def get_monitor_history(monitor_id: int):
    history = []
    for check in check_history:
        if check["monitor_id"] == monitor_id:
            history.append(check)
    return history

@app.delete("/monitors/{monitor_id}")
def delete_monitor(monitor_id: int):
    monitor = find_monitor(monitor_id)
    if not monitor:
        return {"error": "Monitor not found"}
    monitors.remove(monitor)
    return {"message": "Monitor deleted"}

@app.put("/monitors/{monitor_id}")
def update_monitor(monitor_id: int, monitor: Monitor):
    m = find_monitor(monitor_id)
    if not m:
        return {"error": "Monitor not found"}
    m["name"] = monitor.name
    m["target"] = monitor.target
    m["port"] = monitor.port
    m["timeout"] = monitor.timeout
    return m