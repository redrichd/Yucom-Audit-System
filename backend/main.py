from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router

app = FastAPI(title="Yucom Audit System API")

# 徹底開放 CORS 權限，解決 GitHub Pages 連線被擋的問題
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def home():
    return {"status": "running", "message": "Yucom Audit API is Live"}