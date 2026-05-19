from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import math

from database import engine, get_db
from models import Base, Player, TrainingSession, SensorData
from schemas import PlayerCreate, SessionCreate, SensorDataCreate

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Soccer Tracker Backend",
    version="1.0"
)

# -------------------------
# CORS (Frontend Connection)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://arise-soccer-tracker-dub9.vercel.app",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Metric Calculations
# -------------------------
def calculate_metrics(data):

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

    speed_estimate = round(
        acceleration_magnitude * 0.8,
        2
    )

    agility_score = min(
        round(rotation_magnitude * 10, 2),
        100
    )

    foot_power_score = min(
        round(acceleration_magnitude * 8, 2),
        100
    )

    touch_detected = (
        1 if acceleration_magnitude > 12
        else 0
    )

    first_touch_detected = (
        1 if acceleration_magnitude > 15
        else 0
    )

    dribble_detected = (
        1
        if acceleration_magnitude > 10
        and rotation_magnitude > 1.5
        else 0
    )

    sprint_detected = (
        1 if acceleration_magnitude > 18
        else 0
    )

    return {
        "acceleration_magnitude":
            round(acceleration_magnitude, 2),

        "speed_estimate":
            speed_estimate,

        "agility_score":
            agility_score,

        "foot_power_score":
            foot_power_score,

        "touch_detected":
            touch_detected,

        "first_touch_detected":
            first_touch_detected,

        "dribble_detected":
            dribble_detected,

        "sprint_detected":
            sprint_detected,
    }


# -------------------------
# Root
# -------------------------
@app.get("/")
def home():
    return {
        "message":
        "Smart Soccer Tracker backend running"
    }


# -------------------------
# Players
# -------------------------
@app.post("/players")
def create_player(
    player: PlayerCreate,
    db: Session = Depends(get_db)
):

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
def get_players(
    db: Session = Depends(get_db)
):
    return db.query(Player).all()


# -------------------------
# Sessions
# -------------------------
@app.post("/sessions")
def create_session(
    session: SessionCreate,
    db: Session = Depends(get_db)
):

    player = (
        db.query(Player)
        .filter(
            Player.id ==
            session.player_id
        )
        .first()
    )

    if not player:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    new_session = TrainingSession(
        player_id=session.player_id,
        session_name=session.session_name
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return {
        "message":
            "Session created",

        "session":
            new_session
    }


@app.get("/sessions")
def get_sessions(
    db: Session = Depends(get_db)
):
    return db.query(
        TrainingSession
    ).all()


# -------------------------
# Sensor Data
# -------------------------
@app.post("/sensor-data")
def receive_sensor_data(
    data: SensorDataCreate,
    db: Session = Depends(get_db)
):

    metrics = calculate_metrics(data)

    new_data = SensorData(
        session_id=data.session_id,

        accel_x=data.accel_x,
        accel_y=data.accel_y,
        accel_z=data.accel_z,

        gyro_x=data.gyro_x,
        gyro_y=data.gyro_y,
        gyro_z=data.gyro_z,

        acceleration_magnitude=
            metrics[
                "acceleration_magnitude"
            ],

        speed_estimate=
            metrics[
                "speed_estimate"
            ],

        agility_score=
            metrics[
                "agility_score"
            ],

        foot_power_score=
            metrics[
                "foot_power_score"
            ],

        touch_detected=
            metrics[
                "touch_detected"
            ],

        first_touch_detected=
            metrics[
                "first_touch_detected"
            ],

        dribble_detected=
            metrics[
                "dribble_detected"
            ],

        sprint_detected=
            metrics[
                "sprint_detected"
            ],
    )

    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return {
        "message":
            "Sensor saved",

        "metrics":
            metrics
    }


@app.get("/sensor-data")
def get_sensor_data(
    db: Session = Depends(get_db)
):
    return db.query(
        SensorData
    ).all()


# -------------------------
# Session Summary
# -------------------------
@app.get(
"/sessions/{session_id}/summary"
)
def session_summary(
    session_id: int,
    db: Session = Depends(get_db)
):

    records = (
        db.query(
            SensorData
        )
        .filter(
            SensorData.session_id ==
            session_id
        )
        .all()
    )

    if not records:
        return {
            "message":
            "No data"
        }

    return {

        "session_id":
            session_id,

        "touches":
            sum(
                r.touch_detected
                for r in records
            ),

        "dribbles":
            sum(
                r.dribble_detected
                for r in records
            ),

        "sprints":
            sum(
                r.sprint_detected
                for r in records
            ),

        "average_speed":
            round(
                sum(
                    r.speed_estimate
                    for r in records
                )
                /
                len(records),
                2
            ),
    }
