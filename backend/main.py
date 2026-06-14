from fastapi import FastAPI
from database import init_db
from routes.monitors import router as monitors_router

app = FastAPI()

init_db()

@app.get("/")
def home():
    return {"message": "Network Status Monitor API is running!!"}

app.include_router(monitors_router)