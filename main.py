import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import api_router
from config import configs
from startup.migrator import DatabaseMigrator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    import db
    logging.info("🚀 start")
    migrator = DatabaseMigrator()
    migrator.run_migrations()
    yield
    db.dispose()
    logging.info("👋 end")

app = FastAPI(
    title=configs.PROJECT_NAME,
    version=configs.VERSION,
    openapi_url=f"{configs.API_BASE_URL}/openapi.json",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix=configs.API_BASE_URL)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=configs.PORT, reload=True)
