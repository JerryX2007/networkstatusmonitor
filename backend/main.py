from fastapi import FastAPI
from pydantic import BaseModel
import socket
import time

app = FastAPI()

class Monitor(BaseModel):
    name: str
    target: str
    port: int = 80
    timeout: float = 3.0


monitors = []

@app.post("/monitors")
def add_monitor(monitor: Monitor):
    new_monitor = {
        "id": len(monitors) + 1,
        "name": monitor.name,
        "target": monitor.target,
        "port": monitor.port,
        "timeout": monitor.timeout
    }
    monitors.append(new_monitor)
    return new_monitor

@app.get("/monitors")
def get_monitors():
    return monitors

@app.get("/monitors/{monitor_id}")
def read_monitor(monitor_id: int):
    for monitor in monitors:
        if monitor["id"] == monitor_id:
            return monitor
    return {"error": "Monitor not found"}

@app.delete("/monitors/{monitor_id}")
def delete_monitor(monitor_id: int):
    for monitor in monitors:
        if monitor["id"] == monitor_id:
            monitors.remove(monitor)
            return {"message": "Monitor deleted"}
    return {"error": "Monitor not found"}

@app.put("/monitors/{monitor_id}")
def update_monitor(monitor_id: int, monitor: Monitor):
    for m in monitors:
        if m["id"] == monitor_id:
            m["name"] = monitor.name
            m["target"] = monitor.target
            m["port"] = monitor.port
            m["timeout"] = monitor.timeout
            return m
    return {"error": "Monitor not found"}

@app.get("/monitors/{monitor_id}/check")
def check_monitor(monitor_id: int):
    for monitor in monitors:
        if monitor["id"] == monitor_id:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(monitor["timeout"])
            start_time = time.perf_counter()
            try:
                sock.connect((monitor["target"], monitor["port"]))
                end_time = time.perf_counter()
                latency = (end_time - start_time) * 1000
                latency = round(latency, 2)
                return {"status": "online", "latency": latency}
            except socket.timeout:
                return {"status": "offline", "error": "Connection timed out"}
            except socket.error as e:
                return {"status": "offline", "error": str(e)}
            finally:
                sock.close()
    return {"error": "Monitor not found"}


"""
@app.get("/")
def home():
    return {"message": "Hello, World!"}


@app.get("/monitors/{monitor_id}")
def read_monitor(monitor_id: int, q: str | None = None):
    return {"monitor_id": monitor_id, "q": q}

@app.put("/monitors/{monitor_id}")
def update_monitor(monitor_id: int, monitor: Monitor):
    return {"monitor_name": monitor.name, "target": monitor.target, "port": monitor.port}
"""
