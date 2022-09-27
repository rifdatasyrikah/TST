from fastapi import FastAPI
from pydantic import BaseModel

import json

app = FastAPI()

class mahasiswa(BaseModel):
    nim: int
    nama: str

list_mahasiswa = []

with open('mahasiswa.json', 'r') as f:
    list_mahasiswa = json.load(f)['mahasiswa']

# print(list_mahasiswa)

@app.post("/")
# menerima data NIM dan nama dar client dalam format JSON
async def add_mahasiswa(M: mahasiswa):
    #disimpan ke dalam sebuah variabel (dictionary)
    new_mahasiswa = {
        "nim":M.nim,
        "nama":M.nama
        }

    #menambahkan data baru ke data mahasiswa yang sudah ada
    list_mahasiswa.append(new_mahasiswa)

    #menyimpan seluruh data ke file JSON
    luaran = {'mahasiswa':list_mahasiswa}
    with open('mahasiswa.json', 'w') as f:
        json.dump(luaran, f)

    return new_mahasiswa

#asumsi input tidak perlu dicek apakah data nim yang diinput sudah ada pada data yang ada sebelumnya