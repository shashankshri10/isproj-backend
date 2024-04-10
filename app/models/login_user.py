from pydantic import BaseModel, Field

class LoginUser(BaseModel):
    email_id: str = Field(pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$') # regex pattern for mail
    password: str = Field(min_length=8)
    user_type: str = Field(pattern=r'^(regular|admin)$') # regex pattern for value
    secret_key: str