from fastapi import APIRouter, Depends, HTTPException
from database.database import get_db, Mahasiswa, Transkrip
import models.mahasiswa as model
from sqlalchemy.orm import Session
from authentication.jwt_bearer import jwtBearer

mahasiswa_router = APIRouter(tags=["Mahasiswa"])

@mahasiswa_router.get("/mahasiswa")
async def retrieve_all_mahasiswa(db: Session= Depends(get_db)):
    db_mahasiswa = db.query(Mahasiswa).all()
    if db_mahasiswa == []:
        raise HTTPException(status_code=404, detail="Tidak ada data mahasiswa dalam database")
    return db_mahasiswa

@mahasiswa_router.get("/{nim}//Transkrip", dependencies=[Depends(jwtBearer())])
async def retrieve_transkrip_mahasiswa(nim: int, db: Session= Depends(get_db)):
    db_transkrip = db.query(Transkrip).filter(Transkrip.nim==nim).all()
    if db_transkrip == []:
        raise HTTPException(status_code=404, detail="Tidak ada data Transkrip historis untuk mahasiswa tersebut")
    return db_transkrip

@mahasiswa_router.post("/{nim}/Transkrip/Add")
async def add_transkrip_mahasiswa(transkrip: model.Transkrip, db: Session= Depends(get_db)):
    db_transkri = db.query(Transkrip).filter(Transkrip.nim==transkrip.nim, Transkrip.semester==transkrip.semester).first()
    if db_transkri is None:    
        new_Transkrip=Transkrip(nim=transkrip.nim, semester=transkrip.semester, jumlah_sks=transkrip.jumlah_sks, ip=transkrip.ip)
        db.add(new_Transkrip)
        db.commit()
        db.refresh(new_Transkrip)
        return new_Transkrip
    else:
        return {"Error":"Data Transkrip tersebut sudah ada di dalam database"}

@mahasiswa_router.delete("/{nim}/Transkrip/Delete")
async def delete_transkrip_mahasiswa(nim: int, semester:int, db: Session=Depends(get_db)):
    db_transkri = db.query(Transkrip).filter(Transkrip.nim==nim, Transkrip.semester==semester).first()
    if db_transkri is None:
        raise HTTPException(status_code=404, detail="Data Transkrip tersebut tidak ada dalam database")
    else:
        db.query(Transkrip).filter(Transkrip.nim==nim, Transkrip.semester==semester).delete()
        db.commit()
        return {"Message":"Data Transkrip berhasil dihapus dari database"}

@mahasiswa_router.get("/{nim}/PrediksiIPK")
async def prediksi_ipk_mahasiswa(nim: int, db: Session=Depends(get_db)):
    return None

