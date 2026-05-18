from fastapi import FastAPI
from app.routers.auth_router import router as auth_router

app = FastAPI(
    title="AI CV Internship Assistant API",
    version="1.0.0"
)

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "AI CV Internship Assistant API is running"}

