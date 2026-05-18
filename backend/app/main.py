from fastapi import FastAPI

app = FastAPI(
    title="AI CV Internship Assistant API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "AI CV Internship Assistant API is running"}