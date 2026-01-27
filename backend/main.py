from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Yucom Audit System API")

# CORS Setup (Allow frontend)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from backend.api.routes import router as api_router
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Yucom Audit System API is running", "service": "yucom-audit-backend"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
