from xbase_util.db.bean.TaskTemplateBean import TaskTemplateBean


class TaskTemplateDao:
    def __init__(self,Session):
        self.Session = Session

    def addTemplate(self, data):
        with self.Session() as session:
            try:
                b = TaskTemplateBean()
                b.config_id = data.config_id
                b.flow_id = data.flow_id
                b.description = data.description
                b.is_scheduled = data.is_scheduled
                b.scheduled_start_time = data.scheduled_start_time
                b.scheduled_interval_minutes = data.scheduled_interval_minutes
                b.scheduled_period_minutes = data.scheduled_period_minutes
                session.add(b)
                session.commit()
            except Exception as e:
                print(e)
                session.rollback()

    def changeTemplate(self, data):
        with self.Session() as session:
            try:
                bean = session.query(TaskTemplateBean).first()
                bean.config_id = data.config_id
                bean.flow_id = data.flow_id
                bean.description = data.description
                session.commit()
            except Exception as e:
                print(e)
                session.rollback()

    def get_list(self):
        with self.Session() as session:
            try:
                temp_list = session.query(TaskTemplateBean).all()
                return temp_list
            except Exception as e:
                session.rollback()
                print(e)
                return []

    def delete_template(self, id):
        with self.Session() as session:
            try:
                bean = session.query(TaskTemplateBean).filter_by(id=id).first()
                session.delete(bean)
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                print(e)
                return False
