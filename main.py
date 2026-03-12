from fastapi import FastAPI
from Database.database import engine,Base
from Route import register_route,login_route,complain_route,department_route
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
load_dotenv()
import os
os.makedirs("uploads", exist_ok=True)
app = FastAPI(docs_url=None, redoc_url=None)
origins = [
    "http://localhost:5173",
    "https://complain-mangement-frontend.vercel.app"
   
   
]

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/media", StaticFiles(directory="uploads"), name="media")
@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(register_route.route)
app.include_router(login_route.route)
app.include_router(complain_route.route)
app.include_router(department_route.route)



if __name__ == "__main__":
     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)


