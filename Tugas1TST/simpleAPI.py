from fastapi import FastAPI
from pydantic import BaseModel

import json

app = FastAPI()

class mahasiswa(BaseModel):
    nim: int
    nama: str

@app.post("/")
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

    return "Data mahasiswa baru: " +str(new_mahasiswa)+ " telah diterima"

#asumsi input tidak perlu dicek apakah data nim yang diinput sudah ada pada data yang ada sebelumnya