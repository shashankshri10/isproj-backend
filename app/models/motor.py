from datetime import datetime
from pydantic import BaseModel

class MotorData(BaseModel):
    timestamp: datetime
    user_id: int
    motor_id: int
    power_rating: int
    location: str