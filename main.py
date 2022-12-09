from fastapi import FastAPI
import uvicorn

from database.database import Base, engine
from routes.user import user_router
from routes.mahasiswa import mahasiswa_router

app = FastAPI()
app.include_router(user_router)
app.include_router(mahasiswa_router)


Base.metadata.create_all(engine)

@app.get("/", tags=["Home"])
async def home():
    return {"Message":"Selamat Datang"}

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)