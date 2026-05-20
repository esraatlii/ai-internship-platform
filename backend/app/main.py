from fastapi import FastAPI
from app.routers.auth_router import router as auth_router
from app.routers.cv_router import router as cv_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI CV Internship Assistant API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5500",
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(cv_router)

@app.get("/")
def root():
    return {"message": "AI CV Internship Assistant API is running"}

