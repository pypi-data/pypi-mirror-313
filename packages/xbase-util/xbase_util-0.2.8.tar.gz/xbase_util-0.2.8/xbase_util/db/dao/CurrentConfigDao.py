from xbase_util.db.bean.CurrentConfigBean import CurrentConfig


class CurrentConfigDao:
    def __init__(self,Session):
        self.Session = Session

    def set_current_config(self, id, desc):
        with self.Session() as session:
            try:
                session.query(CurrentConfig).delete()
                session.add(CurrentConfig(config_id=id, description=desc))
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Error: {e}")

    def get_current_config(self):
        with self.Session() as session:
            try:
                return session.query(CurrentConfig).first()
            except Exception as e:
                session.rollback()
                print(f"Error: {e}")