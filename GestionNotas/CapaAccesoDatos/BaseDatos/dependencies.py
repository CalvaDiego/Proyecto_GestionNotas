from sqlalchemy.orm import Session
from CapaAccesoDatos.BaseDatos.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
