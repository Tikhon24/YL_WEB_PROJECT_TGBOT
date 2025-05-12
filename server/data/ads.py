import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Ads(SqlAlchemyBase, SerializerMixin):
    """Шаблон бд для объявлений в канале"""
    __tablename__ = 'ads'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    # поле картинки
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    user_tag = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    ads_id = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    message_id = sqlalchemy.Column(sqlalchemy.String, nullable=False)
