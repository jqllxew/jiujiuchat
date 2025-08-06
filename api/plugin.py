import logging
import re
from typing import Any

import httpx
import yaml
from fastapi import Depends, APIRouter, Request

from api.component.auth import get_lobe_user
from config import configs
from config.manifest import ocr, clothes

router = APIRouter()


@router.get("/manifest/{name}.json", summary="插件清单映射")
async def manifest(
    *,
    name: str,
) -> Any:
    with open(f"manifest/{name}.yaml", "r", encoding="utf-8") as f:
        content = f.read()
        new_content = re.sub(r"\$\{(\w+)\}", lambda x: getattr(configs, x.group(1)), content)
        return yaml.safe_load(new_content)


@router.api_route("/gateway", methods=["POST"], summary="插件网关")
async def gateway(
    *,
    _=Depends(get_lobe_user),
    req: Request
) -> Any:
    async with httpx.AsyncClient() as client:
        method = req.method
        data = await req.json()
        api_name = data.get("apiName", "")
        api_list = data.get("manifest", {}).get("api", [])
        api_url = next((x.get("url") for x in api_list if x.get("name") == api_name), None)
        body = data.get("arguments", {}).encode("utf-8")
        headers = dict(req.headers)
        headers.pop("content-length", None)
        resp = await client.request(method, api_url, headers=headers, content=body)
        resp_data = resp.json()
        logging.info("gateway resp: %s", resp_data)
        return resp_data


@router.post("/clothes")
async def get_clothes(
    *,
    req: Request,
    _=Depends(get_lobe_user)
):
    args = await req.json()
    logging.info("get_clothes args: %s", args)
    return clothes.get_clothes(**args)


@router.post("/volcengine-ocr")
async def get_volcengine_ocr(
    *,
    req: Request,
    _=Depends(get_lobe_user)
):
    args = await req.json()
    logging.info("get_volcengine_ocr args: %s", args)
    return ocr.handle(**args)
