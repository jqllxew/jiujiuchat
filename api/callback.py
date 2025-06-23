import xmltodict
from fastapi import APIRouter, Request
from starlette.responses import PlainTextResponse
from wechatpy.crypto import WeChatCrypto

from config import configs

router = APIRouter()
crypto = WeChatCrypto(configs.QW_TOKEN, configs.QW_ENCODING_AES_KEY, configs.QW_CORP_ID)


@router.get("/")
async def callback_check(req: Request):
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
        print("验证失败:", e)
        return PlainTextResponse("error", status_code=400)


@router.post("/")
async def callback(req: Request):
    return PlainTextResponse("ok", status_code=200)
