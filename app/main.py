from fastapi import FastAPI

from app.api import routes_assets, routes_detections, routes_media, routes_users

app = FastAPI(
    title="Asset Tracker API",
    description="API for tracking and managing assets with detection capabilities",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(routes_assets.router)
app.include_router(routes_users.router)
app.include_router(routes_detections.router)
app.include_router(routes_media.router)


@app.get("/")
def read_root():
    return {"message": "API is up"}
