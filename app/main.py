from fastapi import FastAPI

app = FastAPI(
    title="TaskFlow API",
    description="A production-grade task management API",
    version="0.1.0",
)

@app.get("/health")
def health_check():
    return {"status":"OK"}

