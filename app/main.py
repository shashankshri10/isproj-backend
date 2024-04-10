from fastapi import FastAPI

from .routes import user
from .routes import motor

app = FastAPI()

app.include_router(user.router)
app.include_router(motor.router)