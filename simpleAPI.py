# from fastapi import FastAPI
from pydantic import BaseModel

import json
# import uvicorn

import uvicorn
from fastapi import FastAPI, Body, Depends
from model import PostSchema, UserLoginSchema, UserSchema
from jwt_handler import signJWT
from jwt_bearer import jwtBearer

app = FastAPI()

class mahasiswa(BaseModel):
    nim: int
    nama: str

class indeks(BaseModel):
    nim: int
    mata_kuliah :str
    sks: int
    indeks: str

users = []



@app.post("/add", dependencies =[Depends(jwtBearer())], tags=["add mahasiswa"])
# menerima data NIM dan nama dar client dalam format JSON
async def add_mahasiswa(M: mahasiswa):
    #inisialisasi list data mahasiswa
    list_mahasiswa = []

    #simpan data dari file JSON ke list
    with open('mahasiswa.json', 'r') as f:
        list_mahasiswa = json.load(f)['mahasiswa']

    #cek isi data awal
    print(list_mahasiswa)

    #disimpan ke dalam sebuah variabel (dictionary)
    new_mahasiswa = {
        "nim":M.nim,
        "nama":M.nama
        }

    # #menambahkan data baru ke data mahasiswa yang sudah ada
    list_mahasiswa.append(new_mahasiswa)

    #cek list data baru
    print(list_mahasiswa)

    #menyimpan seluruh data ke file JSON
    luaran = {'mahasiswa':list_mahasiswa}
    with open('mahasiswa.json', 'w') as f:
        json.dump(luaran, f)

    return {"message": "data mahasiswa berhasil ditambahkan"}


@app.post("/{nim}",dependencies =[Depends(jwtBearer())], tags=["prediksi ipk"])
# menerima data NIM dan nama dar client dalam format JSON
async def add_indeks(I: indeks):
    #inisialisasi list data mahasiswa
    list_indeks = []

    #simpan data dari file JSON ke list
    with open('indeks.json', 'r') as f:
        list_indeks = json.load(f)['indeks']

    #cek isi data awal
    print(list_indeks)

    #disimpan ke dalam sebuah variabel (dictionary)
    new_indeks = {
        "mata_kuliah":I.mata_kuliah,
        "sks":I.sks,
        "indeks":I.indeks
        }

    # #menambahkan data baru ke data mahasiswa yang sudah ada
    list_indeks.append(new_indeks)

    #cek list data baru
    print(list_indeks)

    #menyimpan seluruh data ke file JSON
    luaran = {'indeks':list_indeks}
    with open('indeks.json', 'w') as f:
        json.dump(luaran, f)

    return {"message": "data indeks berhasil ditambahkan"}
#asumsi input tidak perlu dicek apakah data nim yang diinput sudah ada pada data yang ada sebelumnya

# 5
@app.post("/user/signup", tags=["user"])
def signup(user : UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        else:
            False

# 6
@app.post("/user/login", tags=["user"])
def login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return {
            "error" : "Invalid"
        }


if __name__ == '__main__':
    uvicorn.run("simpleAPI:app", host="0.0.0.0", port=8000, reload=True)