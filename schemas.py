from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PlayerCreate(BaseModel):
    name: str
    position: Optional[str] = None
    dominant_foot: Optional[str] = None


class PlayerResponse(BaseModel):
    id: int
    name: str
    position: Optional[str] = None
    dominant_foot: Optional[str] = None
    
    class Config:
        from_attributes = True
        
class SessionCreate(BaseModel):
    player_id: int
    session_name: Optional[str] = "Training Session"

    
class SessionResponse(BaseModel):
    id: int
    player_id: int
    session_name: str
    start_time: datetime
    end_time: Optional[datetime]
    
    class Config:
        from_attributes = True

class SensorDataCreate(BaseModel):
    session_id: int
    
    accel_x: float
    accel_y: float
    accel_z: float
    
    gyro_x: float
    gyro_y: float
    gyro_z: float
    
class SensorDataResponse(BaseModel):
    id: int
    session_id: int
    
    accel_x: float
    accel_y: float
    accel_z: float
    
    gyro_x: float
    gyro_y: float
    gyro_z: float

    acceleration_magnitude: float
    speed_estimate: float
    agility_score: float
    foot_power_score: float
    
    touch_detected: int
    first_touch_detected: int
    dribble_detected: int
    sprint_detected: int
    
    timestamp: datetime
    
    class Config:
        from_attributes = True
        

    
