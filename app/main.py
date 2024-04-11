from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import user
from .routes import motor

app = FastAPI()

# origins = [
#     "http://localhost:3000"
# ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(motor.router)