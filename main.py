from sduop_be.admin.authz_status.routes import router as status_router
from sduop_be.admin.audit.routes import router as bitacora_router

from fastapi import FastAPI
app = FastAPI(title="Backend Service", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/hello")
def hello(name: str = "world"):
    return {"message": f"Hello, {name}!"}

@app.get("/Dali")
def Dali(name: str = "Dali"):
    return {"message": f"Hello, {name}!"}

app.include_router(status_router, prefix="/data_status", tags=["data_status"])
app.include_router(bitacora_router)