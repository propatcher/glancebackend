from fastapi import FastAPI
import sys
from database.config import settings

app = FastAPI()

@app.get("/")
async def root():
    return {"glance" : True}