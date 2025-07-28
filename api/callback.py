import logging

import xmltodict
from fastapi import APIRouter, Request, Depends
from starlette.responses import PlainTextResponse
from wechatpy.crypto import WeChatCrypto

from config import configs
from services import get_service, TokenService

router = APIRouter()
crypto = WeChatCrypto(configs.QW_TOKEN, configs.QW_ENCODING_AES_KEY, configs.QW_CORP_ID)


@router.get("/test")
async def test_get_token(
    token_service: TokenService = Depends(get_service(TokenService))
):
    token = await token_service.get_token()
    return token


@router.get("/")
async def callback_check(req: Request):
    logging.info("回调校验")
    params = req.query_params
    msg_signature = params.get("msg_signature")
    timestamp = params.get("timestamp")
    nonce = params.get("nonce")
    echostr = params.get("echostr")
    # 构造 XML
    xml = f"""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <Encrypt><![CDATA[{echostr}]]></Encrypt>
        </xml>
        """
    try:
        # 解密 echostr 得到明文
        plain = crypto.decrypt_message(xml, msg_signature, timestamp, nonce)
        return PlainTextResponse(plain)
    except Exception as e:
        logging.error("验证失败: ", e)
        return PlainTextResponse("error", status_code=400)


@router.post("/")
async def callback(
    req: Request,
    token_service: TokenService = Depends(get_service(TokenService))
):
    body_bytes = await req.body()
    body_str = body_bytes.decode("utf-8")
    try:
        body_dict = xmltodict.parse(body_str)
        encrypt = body_dict["xml"]["Encrypt"]
    except Exception as e:
        logging.error(f"解析加密消息失败: {e}")
        return PlainTextResponse("error", status_code=400)

    params = req.query_params
    msg_signature = params.get("msg_signature")
    timestamp = params.get("timestamp")
    nonce = params.get("nonce")

    xml_for_decrypt = f"""
        <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <Encrypt><![CDATA[{encrypt}]]></Encrypt>
        </xml>
        """

    try:
        plain_xml = crypto.decrypt_message(xml_for_decrypt, msg_signature, timestamp, nonce)
        logging.info(f"解密后的明文：\n{plain_xml}")

        plain_dict = xmltodict.parse(plain_xml)
        xml = plain_dict["xml"]

    except Exception as e:
        logging.error(f"解密失败: {e}")
        return PlainTextResponse("error", status_code=400)
    return PlainTextResponse("success", status_code=200)
