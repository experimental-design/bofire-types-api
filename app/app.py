from fastapi import FastAPI
from routers import types_router, versions_router
from routers.versions import router as versions_router

app = FastAPI(
    title="BoFire Types API",
    version="0.0.1",
    root_path="/",
)

app.include_router(types_router)
app.include_router(versions_router)
