from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, BigInteger, String, DateTime

from models.base import Base, TimestampMixin


class QwAccessToken(Base, TimestampMixin):
    __tablename__ = "qw_access_token"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    access_token = Column(String, nullable=False)
    _expires_in = Column("expires_in", Integer, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    @property
    def expires_in(self):
        return self._expires_in

    @expires_in.setter
    def expires_in(self, value):
        self._expires_in = value
        self.expires_at = datetime.utcnow() + timedelta(seconds=value)
