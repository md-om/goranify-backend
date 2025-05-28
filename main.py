# goranify-backend/main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to Kurdish Music Downloader Backend!"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Backend is up and running!"}