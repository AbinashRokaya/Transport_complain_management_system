from fastapi import FastAPI
from Database.database import engine,Base
from Route import register_route,login_route
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5501",
    "http://localhost:5501",
    "https://your-frontend.onrender.com",  # add this
]

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(register_route.route)
app.include_router(login_route.route)



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, loop="asyncio", )


