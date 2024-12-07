from sqlalchemy import Column, Integer,String

from xbase_util.db.bean import DbBase


class CurrentConfig(DbBase):
    __tablename__ = 'currentconfig'
    id = Column(Integer, primary_key=True)
    config_id = Column(Integer)
    description = Column(String)