from datetime import datetime
from pydantic import BaseModel,Field

class MotorData(BaseModel):
    # timestamp: datetime
    # user_id: int = Field(exclude=True)
    motor_id: int
    power_rating: int
    location: str