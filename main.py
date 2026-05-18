from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import math
from fastapi import HTTPException

from database import engine, get_db
from models import Base, Player, TrainingSession, SensorData
from schemas import PlayerCreate, SessionCreate, SensorDataCreate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Soccer Tracker Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def calculate_metrics(data: SensorDataCreate):
    acceleration_magnitude = math.sqrt(
        data.accel_x ** 2 +
        data.accel_y ** 2 +
        data.accel_z ** 2
    )

    rotation_magnitude = math.sqrt(
        data.gyro_x ** 2 +
        data.gyro_y ** 2 +
        data.gyro_z ** 2
    )

    speed_estimate = round(acceleration_magnitude * 0.8, 2)

    agility_score = min(round(rotation_magnitude * 10, 2), 100)

    foot_power_score = min(round(acceleration_magnitude * 8, 2), 100)

    touch_detected = 1 if acceleration_magnitude > 12 else 0

    first_touch_detected = 1 if acceleration_magnitude > 15 else 0

    dribble_detected = 1 if acceleration_magnitude > 10 and rotation_magnitude > 1.5 else 0

    sprint_detected = 1 if acceleration_magnitude > 18 else 0

    return {
        "acceleration_magnitude": round(acceleration_magnitude, 2),
        "speed_estimate": speed_estimate,
        "agility_score": agility_score,
        "foot_power_score": foot_power_score,
        "touch_detected": touch_detected,
        "first_touch_detected": first_touch_detected,
        "dribble_detected": dribble_detected,
        "sprint_detected": sprint_detected,
    }


@app.get("/")
def home():
    return {"message": "Smart Soccer Tracker backend running"}


@app.post("/players")
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    new_player = Player(
        name=player.name,
        position=player.position,
        dominant_foot=player.dominant_foot
    )

    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    return new_player


@app.get("/players")
def get_players(db: Session = Depends(get_db)):
    return db.query(Player).all()


@app.post("/sessions")
def create_session(session: SessionCreate, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == session.player_id).first()

    if player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found. Create a player first."
        )

    new_session = TrainingSession(
        player_id=session.player_id,
        session_name=session.session_name
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return {
        "message": "Session created successfully",
        "session_id": new_session.id,
        "player_id": new_session.player_id,
        "session_name": new_session.session_name,
        "start_time": new_session.start_time
    }


@app.get("/sessions")
def get_sessions(db: Session = Depends(get_db)):
    return db.query(TrainingSession).all()


@app.post("/sensor-data")
def receive_sensor_data(data: SensorDataCreate, db: Session = Depends(get_db)):
    metrics = calculate_metrics(data)

    new_data = SensorData(
        session_id=data.session_id,

        accel_x=data.accel_x,
        accel_y=data.accel_y,
        accel_z=data.accel_z,

        gyro_x=data.gyro_x,
        gyro_y=data.gyro_y,
        gyro_z=data.gyro_z,

        acceleration_magnitude=metrics["acceleration_magnitude"],
        speed_estimate=metrics["speed_estimate"],
        agility_score=metrics["agility_score"],
        foot_power_score=metrics["foot_power_score"],

        touch_detected=metrics["touch_detected"],
        first_touch_detected=metrics["first_touch_detected"],
        dribble_detected=metrics["dribble_detected"],
        sprint_detected=metrics["sprint_detected"],
    )

    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return {
        "message": "Sensor data saved successfully",
        "metrics": metrics,
        "data": new_data
    }


@app.get("/sensor-data")
def get_sensor_data(db: Session = Depends(get_db)):
    return db.query(SensorData).all()


@app.get("/sessions/{session_id}/summary")
def get_session_summary(session_id: int, db: Session = Depends(get_db)):
    records = db.query(SensorData).filter(
        SensorData.session_id == session_id
    ).all()

    if not records:
        return {"message": "No data found for this session"}

    total_touches = sum(record.touch_detected for record in records)
    total_first_touches = sum(record.first_touch_detected for record in records)
    total_dribbles = sum(record.dribble_detected for record in records)
    total_sprints = sum(record.sprint_detected for record in records)

    avg_speed = sum(record.speed_estimate for record in records) / len(records)
    avg_agility = sum(record.agility_score for record in records) / len(records)
    avg_foot_power = sum(record.foot_power_score for record in records) / len(records)
    max_acceleration = max(record.acceleration_magnitude for record in records)

    return {
        "session_id": session_id,
        "total_data_points": len(records),
        "total_touches": total_touches,
        "total_first_touches": total_first_touches,
        "total_dribbles": total_dribbles,
        "total_sprints": total_sprints,
        "average_speed_estimate": round(avg_speed, 2),
        "average_agility_score": round(avg_agility, 2),
        "average_foot_power_score": round(avg_foot_power, 2),
        "max_acceleration": round(max_acceleration, 2)
    }