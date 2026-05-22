from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, Player, TrainingSession, TrackerData
from schemas import PlayerSignup, PlayerLogin, SessionCreate, TrackerDataCreate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ARISE Soccer Tracker Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "ARISE backend running"}


@app.post("/signup")
def signup(player: PlayerSignup, db: Session = Depends(get_db)):
    existing = db.query(Player).filter(Player.email == player.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_player = Player(
        name=player.name,
        email=player.email,
        password=player.password,
        position=player.position,
        dominant_foot=player.dominant_foot
    )

    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    return {
        "message": "Account created",
        "player_id": new_player.id,
        "name": new_player.name,
        "email": new_player.email,
        "position": new_player.position,
        "dominant_foot": new_player.dominant_foot
    }


@app.post("/login")
def login(player: PlayerLogin, db: Session = Depends(get_db)):
    existing = db.query(Player).filter(Player.email == player.email).first()

    if not existing or existing.password != player.password:
        raise HTTPException(status_code=401, detail="Invalid login")

    return {
        "message": "Login successful",
        "player_id": existing.id,
        "name": existing.name,
        "email": existing.email,
        "position": existing.position,
        "dominant_foot": existing.dominant_foot
    }


@app.get("/players")
def get_players(db: Session = Depends(get_db)):
    return db.query(Player).all()


@app.post("/sessions")
def create_session(session: SessionCreate, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == session.player_id).first()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    new_session = TrainingSession(
        player_id=session.player_id,
        session_name=session.session_name
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session


@app.get("/sessions")
def get_sessions(db: Session = Depends(get_db)):
    return db.query(TrainingSession).all()


def calculate_soccer_metrics(acceleration: float, speed: float, activity: str):
    touches = 0
    dribbles = 0
    sprints = 0

    if activity in ["Walking", "Jogging"]:
        touches = 1

    if activity == "Jogging":
        dribbles = 1

    if activity == "Sprint":
        sprints = 1

    agility_score = min(acceleration * 18, 100)
    foot_power_score = min(acceleration * 15, 100)
    first_touch_score = min(speed * 12, 100)

    return {
        "touches": touches,
        "dribbles": dribbles,
        "sprints": sprints,
        "agility_score": round(agility_score, 2),
        "foot_power_score": round(foot_power_score, 2),
        "first_touch_score": round(first_touch_score, 2)
    }


@app.post("/tracker-data")
def receive_tracker_data(data: TrackerDataCreate, db: Session = Depends(get_db)):
    session = db.query(TrainingSession).filter(
        TrainingSession.id == data.session_id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    metrics = calculate_soccer_metrics(
        data.acceleration,
        data.speed,
        data.activity
    )

    new_data = TrackerData(
        player_id=data.player_id,
        session_id=data.session_id,
        acceleration=data.acceleration,
        speed=data.speed,
        activity=data.activity,
        touches=metrics["touches"],
        dribbles=metrics["dribbles"],
        sprints=metrics["sprints"],
        agility_score=metrics["agility_score"],
        foot_power_score=metrics["foot_power_score"],
        first_touch_score=metrics["first_touch_score"]
    )

    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return {
        "message": "Tracker data saved",
        "data": new_data
    }


@app.get("/tracker-data")
def get_tracker_data(db: Session = Depends(get_db)):
    return db.query(TrackerData).all()


@app.get("/sessions/{session_id}/summary")
def session_summary(session_id: int, db: Session = Depends(get_db)):
    records = db.query(TrackerData).filter(
        TrackerData.session_id == session_id
    ).all()

    if not records:
        return {
            "message": "No tracker data found",
            "session_id": session_id
        }

    total_touches = sum(r.touches for r in records)
    total_dribbles = sum(r.dribbles for r in records)
    total_sprints = sum(r.sprints for r in records)

    avg_speed = sum(r.speed for r in records) / len(records)
    avg_acceleration = sum(r.acceleration for r in records) / len(records)
    avg_agility = sum(r.agility_score for r in records) / len(records)
    avg_power = sum(r.foot_power_score for r in records) / len(records)
    avg_first_touch = sum(r.first_touch_score for r in records) / len(records)

    latest_activity = records[-1].activity

    return {
        "session_id": session_id,
        "total_records": len(records),
        "total_touches": total_touches,
        "total_dribbles": total_dribbles,
        "total_sprints": total_sprints,
        "average_speed": round(avg_speed, 2),
        "average_acceleration": round(avg_acceleration, 2),
        "average_agility_score": round(avg_agility, 2),
        "average_foot_power_score": round(avg_power, 2),
        "average_first_touch_score": round(avg_first_touch, 2),
        "latest_activity": latest_activity
    }
