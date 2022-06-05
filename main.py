from fastapi import FastAPI

from db import database
from resources import routes

app = FastAPI()
app.include_router(routes.api_router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
