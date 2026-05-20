from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    position = Column(String, nullable=True)
    dominant_foot = Column(String, nullable=True)

    sessions = relationship("TrainingSession", back_populates="player")


class TrainingSession(Base):
    __tablename__ = "training_sessions"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    session_time = Column(String, default="Training Session")
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)

    player = relationship("Player", back_populates="sessions")
    sensor_data = relationship("SensorData", back_populates="session")


class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("training_sessions.id"), nullable=False)

    accel_x = Column(Float, nullable=False)
    accel_y = Column(Float, nullable=False)
    accel_z = Column(Float, nullable=False)

    gyro_x = Column(Float, nullable=False)
    gyro_y = Column(Float, nullable=False)
    gyro_z = Column(Float, nullable=False)

    acceleration_magnitude = Column(Float, default=0.0)

    speed_estimate = Column(Float, default=0.0)
    agility_score = Column(Float, default=0.0)
    foot_power_score = Column(Float, default=0.0)

    touch_detected = Column(Integer, default=0)
    first_touch_detected = Column(Integer, default=0)
    dribble_detected = Column(Integer, default=0)
    sprint_detected = Column(Integer, default=0)

    timestamp = Column(DateTime, default=datetime.utcnow)

    session = relationship("TrainingSession", back_populates="sensor_data")
