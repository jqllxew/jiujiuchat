import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from starlette.middleware.cors import CORSMiddleware

from api import api_router
from config import configs
from config.exc import validation_exception_handler, service_exception_handler, global_exception_handler, \
    ServiceException
from startup.migrator import DatabaseMigrator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    import db
    logging.info("🚀 start")
    app.state.redis = db.redis_client  # type: ignore
    migrator = DatabaseMigrator()
    migrator.run_migrations()
    yield
    await db.dispose()
    logging.info("👋 end")

app = FastAPI(
    title=configs.PROJECT_NAME,
    version=configs.VERSION,
    openapi_url=f"{configs.API_BASE_URL}/openapi.json",
    lifespan=lifespan,
    docs_url=None
)
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix=configs.API_BASE_URL)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ServiceException, service_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_docs():
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title="啾啾API",
        swagger_js_url="https://jiujiuchat.oss-cn-chengdu.aliyuncs.com/swagger-ui-bundle.js",
        swagger_css_url="https://jiujiuchat.oss-cn-chengdu.aliyuncs.com/swagger-ui.css",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=configs.PORT)
