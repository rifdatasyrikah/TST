from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float

SQLALCHEMY_DATABASE_URL = "sqlite:///./Akademik.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine,autocommit=False, autoflush=False,)

Base=declarative_base()

def get_db():
        db=SessionLocal()
        try:
                yield db
        finally:
                db.close()

class User(Base):
    __tablename__="User"
    nim=Column(Integer, primary_key=True)
    email=Column(String, primary_key=True)
    password=Column(String)

class Mahasiswa(Base):
    __tablename__="Mahasiswa"
    nim=Column(Integer, primary_key=True)
    nama=Column(String)

class Transkrip(Base):
    __tablename__="Transkrip"
    nim=Column(Integer, primary_key=True)
    semester=Column(Integer, primary_key=True)
    jumlah_sks=Column(Integer)
    ip=Column(Float)

class PendaftaranPascasarjana(Base):
    __tablename__="PendaftaranPascasarjana"
    id = Column(Integer, primary_key=True, index=True)
    GRE = Column(Integer)
    TOEFL = Column(Integer)
    UniversityRating = Column(Integer)
    SOP = Column(Integer)
    LOR = Column(Integer)
    CGPA = Column(Float)
    Research = Column(Integer)
    Prediction = Column(Float)