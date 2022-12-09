from fastapi import APIRouter, Depends, HTTPException
from database.database import get_db, Mahasiswa, Transkrip, PendaftaranPascasarjana
import models.mahasiswa as model
from sqlalchemy.orm import Session
from authentication.jwt_bearer import jwtBearer

import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
import pickle

mahasiswa_router = APIRouter(tags=["Mahasiswa"])

@mahasiswa_router.get("/mahasiswa")
async def retrieve_all_mahasiswa(db: Session= Depends(get_db)):
    db_mahasiswa = db.query(Mahasiswa).all()
    if db_mahasiswa == []:
        raise HTTPException(status_code=404, detail="Tidak ada data mahasiswa dalam database")
    return db_mahasiswa

@mahasiswa_router.get("/{nim}/Transkrip", dependencies=[Depends(jwtBearer())])
async def retrieve_transkrip_mahasiswa(nim: int, db: Session= Depends(get_db)):
    db_transkrip = db.query(Transkrip).filter(Transkrip.nim==nim).all()
    if db_transkrip == []:
        raise HTTPException(status_code=404, detail="Tidak ada data Transkrip historis untuk mahasiswa tersebut")
    return db_transkrip

@mahasiswa_router.post("/{nim}/Transkrip/Add", dependencies=[Depends(jwtBearer())])
async def add_transkrip_mahasiswa(nim: int, transkrip: model.Transkrip, db: Session= Depends(get_db)):
    db_transkri = db.query(Transkrip).filter(Transkrip.nim==nim, Transkrip.semester==transkrip.semester).first()
    if db_transkri is None:    
        new_Transkrip=Transkrip(nim=nim, semester=transkrip.semester, jumlah_sks=transkrip.jumlah_sks, ip=transkrip.ip)
        db.add(new_Transkrip)
        db.commit()
        db.refresh(new_Transkrip)
        return {"Message": "Data Transkrip berhasil ditambahkan ke database"}
    else:
        return {"Error":"Data Transkrip tersebut sudah ada di dalam database"}

@mahasiswa_router.delete("/{nim}/Transkrip/Delete", dependencies=[Depends(jwtBearer())])
async def delete_transkrip_mahasiswa(nim: int, semester:int, db: Session=Depends(get_db)):
    db_transkrip = db.query(Transkrip).filter(Transkrip.nim==nim, Transkrip.semester==semester).first()
    if db_transkrip is None:
        raise HTTPException(status_code=404, detail="Data Transkrip tersebut tidak ada dalam database")
    else:
        db.query(Transkrip).filter(Transkrip.nim==nim, Transkrip.semester==semester).delete()
        db.commit()
        return {"Message":"Data Transkrip berhasil dihapus dari database"}

@mahasiswa_router.get("/{nim}/Prediksi/IPK", dependencies=[Depends(jwtBearer())])
async def prediksi_ipk_mahasiswa(nim: int, db: Session=Depends(get_db)):
    db_transkrip = db.query(Transkrip).filter(Transkrip.nim==nim).all()
    if db_transkrip == []:
        return {"Error":"Data Transkrip untuk mahasiswa tersebut tidak ada di dalam database"}
    else:   
        total = 0 
        for data in db_transkrip:
            total = data.ip
        
        for i in range(8-len(db_transkrip)):
            total += 3
        
        prediksi = total/8
        return {"prediksi IPK" : prediksi}

@mahasiswa_router.post("/Prediksi/AdmisiPascasarjana", dependencies=[Depends(jwtBearer())])
async def prediksi_admisi_pascasarjana(data : model.dataPendaftaran, db: Session=Depends(get_db)):
    print(data)
    arrX = np.array([[data.GRE, data.TOEFL, data.UniversityRating, data.SOP, data.LOR, data.CGPA, data.Research]]).astype(float)
    print(arrX)
    pickle_in = open("admition.pickle", "rb") 
    model = pickle.load(pickle_in)

    prediction = model.predict(arrX)

    new_pendaftaran=PendaftaranPascasarjana(GRE=data.GRE, TOEFL=data.TOEFL, UniversityRating=data.UniversityRating, \
            SOP=data.SOP, LOR=data.LOR, CGPA=data.CGPA, Research=data.Research, Prediction=prediction[0].astype(float))
    # new_pendaftaran=PendaftaranPascasarjana(**data.dict())
    db.add(new_pendaftaran)
    db.commit()
    db.refresh(new_pendaftaran)

    print(prediction)
    return {"prediction" : prediction[0].astype(float)}

@mahasiswa_router.get("/DataPrediksi/AdmisiPascasarjana", dependencies=[Depends(jwtBearer())])
async def retrieve_data_prediksi_admisi_pascasarjana(db: Session=Depends(get_db)):
    data = db.query(PendaftaranPascasarjana).all()
    return data