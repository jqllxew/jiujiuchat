import hashlib
import logging
from pathlib import Path

import alibabacloud_oss_v2 as oss
from alibabacloud_oss_v2.credentials import StaticCredentialsProvider
from fastapi import APIRouter, Depends, UploadFile, File
from config import configs
from services import get_lobe_user

router = APIRouter()

cfg = oss.config.load_default()
cfg.credentials_provider = StaticCredentialsProvider(configs.OSS_ACCESS_KEY_ID, configs.OSS_ACCESS_KEY_SECRET)
cfg.region = configs.OSS_REGION
cfg.endpoint = configs.OSS_ENDPOINT
client = oss.Client(cfg)


@router.post("/upload", summary="文件上传")
async def upload(
    *,
    _=Depends(get_lobe_user),
    file: UploadFile = File(...),
):
    data = await file.read()
    if not data:
        return {"msg": "file empty"}
    suffix = Path(file.filename).suffix
    md5 = hashlib.md5(data).hexdigest()
    result = client.put_object(oss.PutObjectRequest(
        bucket=configs.OSS_BUCKET,
        key=f"image/{md5}{suffix}",
        body=data,
    ))
    if result.status_code == 200:
        logging.info(
            f'status code: {result.status_code},'
            f' request id: {result.request_id},'
            f' content md5: {result.content_md5},'
            f' etag: {result.etag},'
            f' hash crc64: {result.hash_crc64},'
            f' version id: {result.version_id},')
        url = f"https://{configs.OSS_BUCKET}.{configs.OSS_ENDPOINT}/image/{md5}{suffix}"
        return {"msg": "file uploaded", "url": url}
    else:
        logging.error(result)
        return {"msg": "upload failed"}
