from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import Base, engine
from .routers import admin, assessment, auth, catalog, me, opportunities

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(catalog.router)
app.include_router(me.router)
app.include_router(admin.router)
app.include_router(assessment.router)
app.include_router(opportunities.router)


@app.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name}
