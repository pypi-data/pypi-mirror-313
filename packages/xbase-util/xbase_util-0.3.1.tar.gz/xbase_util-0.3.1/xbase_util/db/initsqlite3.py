from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from xbase_util.db.bean import DbBase
from xbase_util.db.dao.ConfigDao import ConfigDao
from xbase_util.db.dao.CurrentConfigDao import CurrentConfigDao
from xbase_util.db.dao.FlowDao import FlowDao
from xbase_util.db.dao.TaskTemplateDao import TaskTemplateDao


def initSqlite3(path: str):
    engine = create_engine(path, echo=False)
    DbBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    flowDao = FlowDao(Session)
    configDao = ConfigDao(Session)
    currentConfigDao = CurrentConfigDao(Session)
    taskTemplateDao = TaskTemplateDao(Session)
    return flowDao, configDao, currentConfigDao, taskTemplateDao
