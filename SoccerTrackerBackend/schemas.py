from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PlayerSignup(BaseModel):
    name: str
    email: str
    password: str
    position: Optional[str] = None
    dominant_foot: Optional[str] = None


class PlayerLogin(BaseModel):
    email: str
    password: str


class SessionCreate(BaseModel):
    player_id: int
    session_name: Optional[str] = "Training Session"


class TrackerDataCreate(BaseModel):
    player_id: int
    session_id: int
    acceleration: float
    speed: float
    activity: str


class TrackerDataResponse(BaseModel):
    id: int
    player_id: int
    session_id: int
    acceleration: float
    speed: float
    activity: str
    touches: int
    dribbles: int
    sprints: int
    agility_score: float
    foot_power_score: float
    first_touch_score: float
    timestamp: datetime

    class Config:
        from_attributes = True
    
