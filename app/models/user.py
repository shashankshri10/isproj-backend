from pydantic import BaseModel, Field
from datetime import datetime

class User(BaseModel):
    # timestamp: datetime = Field(default_factory=lambda:datetime.now())
    # user_id: str  
    user_name: str 
    password: str = Field(min_length=8)
    user_type: str = Field(pattern=r'^(regular|admin)$') # regex pattern for value
    designation: str
    email_id: str = Field(pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$') # regex pattern for mail
