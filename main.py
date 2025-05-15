import logging

import uvicorn
from fastapi import FastAPI

from config import Configs

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title=Configs.PROJECT_NAME,
    version=Configs.VERSION,
    openapi_url=f"{Configs.API_BASE_URL}/openapi.json",
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=Configs.PORT)
