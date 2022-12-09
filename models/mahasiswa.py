from typing import List
from pydantic import BaseModel

class Mahasiswa(BaseModel):
    nim: int
    nama: str

class Transkrip(BaseModel):
    # nim: int
    semester: int
    jumlah_sks: int
    ip: float

class dataPendaftaran(BaseModel):
    GRE : int
    TOEFL: int
    UniversityRating : int
    SOP: int
    LOR: int
    CGPA: float
    Research : int