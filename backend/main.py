from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Monitor(BaseModel):
    name: str
    target: str
    port: int = 80

monitors = []

@app.post("/monitors")
def add_monitor(monitor: Monitor):
    new_monitor = {
        "id": len(monitors) + 1,
        "name": monitor.name,
        "target": monitor.target,
        "port": monitor.port
    }
    monitors.append(new_monitor)
    return new_monitor


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
