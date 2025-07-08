from datetime import datetime, timedelta

import requests

from config import configs
from models import QwAccessToken
from services.base import BaseService


class TokenService(BaseService):

    def get_token(self) -> QwAccessToken:
        token = self.db.query(QwAccessToken).filter(
            QwAccessToken.expires_at > datetime.now() - timedelta(seconds=10)
        ).order_by(
            QwAccessToken.expires_at.desc()
        ).first()
        if token is None:
            resp = requests.get("https://qyapi.weixin.qq.com/cgi-bin/gettoken", params={
                "corpid": configs.QW_CORP_ID,
                "corpsecret": configs.QW_CORP_SECRET,
            }, timeout=10)
            resp.raise_for_status()
            res_data = resp.json()
            token = QwAccessToken()
            token.expires_in = res_data.get("expires_in")
            token.access_token = res_data.get("access_token")
            self.db.add(token)
            self.db.commit()
        assert isinstance(token, QwAccessToken)
        return token
