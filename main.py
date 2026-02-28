from fastapi import FastAPI
from Database.database import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)
@app.get("/")
async def root():
    return {"message": "Hello World"}