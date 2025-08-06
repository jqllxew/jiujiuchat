from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, BigInteger, String, DateTime

from .base import Base, TimestampMixin


class QwAccessToken(Base, TimestampMixin):
    __tablename__ = "qw_access_token"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    access_token = Column(String, nullable=False, comment="企业微信Token")
    _expires_in = Column("expires_in", Integer, nullable=False, comment="过期时长/s")
    expires_at = Column(DateTime, nullable=False, comment="过期时间")

    @property
    def expires_in(self):
        return self._expires_in

    @expires_in.setter
    def expires_in(self, value):
        self._expires_in = value
        self.expires_at = datetime.now() + timedelta(seconds=value)
