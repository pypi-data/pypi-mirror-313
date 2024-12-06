"""塞米控数据表模型."""
import datetime

from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import declarative_base


BASE = declarative_base()


# pylint: disable=R0903, disable=W0108
class DbcLinkTray(BASE):
    """DbcLinkTray class."""
    __tablename__ = "dbc_link_tray"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    dbc_code = Column(String(50), nullable=True)
    dbc_state = Column(Integer, nullable=True)
    tray_code = Column(String(50), nullable=True)
    tray_index = Column(Integer, nullable=True)
    lot_name = Column(String(50), nullable=True)
    lot_article_name = Column(String(50))
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(), onupdate=lambda: datetime.datetime.now())
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())

    def as_dict(self):
        """获取字典形式的数据."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns.values()}


class LotInfo(BASE):
    """LotInfo class."""
    __tablename__ = "lot_info"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    lot_name = Column(String(50), nullable=True)
    lot_article_name = Column(String(50), nullable=True)
    lot_quality = Column(Integer, nullable=True)
    lot_state = Column(Integer, nullable=True, default=1)
    recipe_name = Column(String(50), nullable=True)
    point_name = Column(String(50), nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(), onupdate=lambda: datetime.datetime.now())
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())

    def as_dict(self):
        """获取字典形式的数据."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns.values()}


class Point(BASE):
    """Point class."""
    __tablename__ = "point"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    point_name = Column(String(50), nullable=True)
    point_state = Column(Integer, nullable=True, default=1)
    x_point = Column(Float, nullable=True, default=0)
    y_point = Column(Float, nullable=True, default=0)
    x_mark_point = Column(Float, nullable=True, default=0)
    y_mark_point = Column(Float, nullable=True, default=0)
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(), onupdate=lambda: datetime.datetime.now())
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())

    def as_dict(self):
        """获取字典形式的数据."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns.values()}


class Recipe(BASE):
    """Recipe class."""
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    recipe_id = Column(Integer, nullable=True)
    recipe_name = Column(String(50), nullable=True)
    recipe_state = Column(Integer, nullable=True, default=1)
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(), onupdate=lambda: datetime.datetime.now())
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())

    def as_dict(self):
        """获取字典形式的数据."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns.values()}
