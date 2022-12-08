from typing import List
from pydantic import BaseModel

class Mahasiswa(BaseModel):
    nim: int
    nama: str

class Transkrip(BaseModel):
    nim: int
    semester: int
    jumlah_sks: int
    ip: float