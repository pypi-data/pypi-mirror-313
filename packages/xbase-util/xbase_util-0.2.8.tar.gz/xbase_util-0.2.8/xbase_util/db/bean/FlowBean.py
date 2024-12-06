from sqlalchemy import Column, Integer, TEXT

from xbase_util.db.bean import DbBase


class FlowBean(DbBase):
    __tablename__ = 'flows'
    id = Column(Integer, primary_key=True)
    description = Column(TEXT)
    step = Column(TEXT)
