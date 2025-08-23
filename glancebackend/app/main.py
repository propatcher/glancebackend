import asyncio
from fastapi import FastAPI
import sys
from databases.database import CreateDropUtils

app = FastAPI()

@app.get("/")
async def root():
    return {"glance" : True}
