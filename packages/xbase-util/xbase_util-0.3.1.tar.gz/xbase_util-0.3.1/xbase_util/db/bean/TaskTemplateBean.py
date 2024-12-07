from sqlalchemy import Column, Integer, String, Boolean

from xbase_util.db.bean import DbBase


class TaskTemplateBean(DbBase):
    __tablename__ = 'tasktemplatebean'
    id = Column(Integer, primary_key=True)

    config_id = Column(String)
    flow_id = Column(String)
    description = Column(String)

    is_scheduled = Column(Boolean, default=False)  # 是否为定时任务
    scheduled_start_time = Column(String, nullable=True)  # 定时任务的开始时间
    scheduled_interval_minutes = Column(Integer, nullable=True)  # 定时任务的执行间隔（以分钟为单位）
    scheduled_period_minutes = Column(Integer, nullable=True)  # 要获取的时间段（以分钟为单位）

    def to_dict(self):
        return {
            "id": self.id,
            "config_id": self.config_id,
            "flow_id": self.flow_id,
            "description": self.description,
            "is_scheduled": self.is_scheduled,
            "start_time": self.scheduled_start_time,
            "interval_minutes": self.scheduled_interval_minutes,
        }
