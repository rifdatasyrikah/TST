from fastapi import APIRouter, Depends, HTTPException
from database.database import get_db
import database.database 
from models.mahasiswa import Mahasiswa, Transkrip
from sqlalchemy.orm import Session

mahasiswa_router = APIRouter(tags=["Mahasiswa"])

@mahasiswa_router.get("/mahasiswa")
async def retrieve_all_mahasiswa(db: Session= Depends(get_db)):
    db_mahasiswa = db.query(database.Mahasiswa)
    if db_mahasiswa is None:
        raise HTTPException(status_code=404, detail="Tidak ada data mahasiswa dalam database")
    return db_mahasiswa
