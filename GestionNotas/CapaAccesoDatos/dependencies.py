from sqlalchemy.orm import Session
from CapaBaseDatos.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
