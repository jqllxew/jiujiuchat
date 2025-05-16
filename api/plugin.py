import re
from typing import Any

import yaml
from fastapi import Depends, APIRouter, Body, Request

from api.auth import get_current_user
from config import configs
from manifest import clothes

router = APIRouter()


@router.get("/manifest/{id}.json")
def get_manifest(
    *,
    id: str,
) -> Any:
    with open(f"manifest/{id}.yaml", "r", encoding="utf-8") as f:
        content = f.read()
    new_content = re.sub(r"\$\{(\w+)\}", lambda x: getattr(configs, x.group(1)), content)
    return yaml.safe_load(new_content)


@router.post("/clothes")
async def get_clothes(
    *,
    current_user=Depends(get_current_user),
    req: Request
) -> Any:
    print(current_user)
    data = await req.json()
    print(data)
    _clothes = clothes.manClothes
    return _clothes["happy"]
