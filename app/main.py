from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.routers_tweets import router as tweets_router
from app.routers_users import router as users_router
from app.routers_media import router as media_router

app = FastAPI(title="Microblog Service", version="1.0.0")

app.include_router(tweets_router)
app.include_router(users_router)
app.include_router(media_router)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", include_in_schema=False)
def root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Backend is running. Swagger at /docs"}
