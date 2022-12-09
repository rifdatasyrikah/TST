from fastapi import APIRouter, Depends, HTTPException
from database.database import get_db, Mahasiswa, Transkrip
import models.mahasiswa as model
from sqlalchemy.orm import Session
from authentication.jwt_bearer import jwtBearer

import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
import pickle
# import matplotlib.pyplot as pyplot
# from matplotlib import style
# from sklearn.utility import shuffle

# data_admisi = pd.read_csv("adm_data.csv", sep=",")

# data_admisi = data_admisi[["GRE Score","TOEFL Score","University Rating","SOP","LOR", "CGPA", "Research", "Chance of Admit"]]
# data_admisi["CGPA"] = data_admisi["CGPA"].apply(lambda x: (x*4)/10) #mengonversi nilai GPA dari rentang 0-10 menjadi 0-4
# predict_admisi = "Chance of Admit"
# # print(data_admisi)
# x = np.array(data_admisi.drop(columns=predict_admisi))
# print(x)
# y = np.array(data_admisi[predict_admisi])
# print(y)

# x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x,y, test_size=0.1)

# pickle_in = open("admition.pickle", "rb") 
# linear = pickle.load(pickle_in)

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

@mahasiswa_router.post("/{nim}/Transkrip/Add", dependencies=[Depends(jwtBearer())])
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

@mahasiswa_router.delete("/{nim}/Transkrip/Semester_{semester}/Delete", dependencies=[Depends(jwtBearer())])
async def delete_transkrip_mahasiswa(nim: int, semester:int, db: Session=Depends(get_db)):
    db_transkri = db.query(Transkrip).filter(Transkrip.nim==nim, Transkrip.semester==semester).first()
    if db_transkri is None:
        raise HTTPException(status_code=404, detail="Data Transkrip tersebut tidak ada dalam database")
    else:
        db.query(Transkrip).filter(Transkrip.nim==nim, Transkrip.semester==semester).delete()
        db.commit()
        return {"Message":"Data Transkrip berhasil dihapus dari database"}

@mahasiswa_router.post("/Prediksi/IPK", dependencies=[Depends(jwtBearer())])
async def prediksi_ipk_mahasiswa(nim: int, db: Session=Depends(get_db)):
    return None

@mahasiswa_router.post("/Prediksi/AdmisiPascasarjana", dependencies=[Depends(jwtBearer())])
async def prediksi_admisi_pascasarjana(data : model.PendaftaranPascasarjana):
    print(data)
    arrX = np.array([[data.GRE, data.TOEFL, data.UniversityRating, data.SOP, data.LOR, data.CGPA, data.Research]]).astype(float)
    print(arrX)
    pickle_in = open("admition.pickle", "rb") 
    model = pickle.load(pickle_in)

    prediction = model.predict(arrX)
    print(prediction)
    return {"prediction" : prediction[0]}