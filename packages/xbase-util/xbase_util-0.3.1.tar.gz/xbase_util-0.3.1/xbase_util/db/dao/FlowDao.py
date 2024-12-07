from xbase_util.db.bean.FlowBean import FlowBean


class FlowDao:
    def __init__(self,Session):
        self.Session = Session

    def add_flow(self, description, step, flow_id=None):
        with self.Session() as session:
            try:
                if flow_id is None:
                    flow = FlowBean(description=description, step=step)
                    session.add(flow)
                else:
                    flow = session.query(FlowBean).filter_by(id=flow_id).first()
                    flow.description = description
                    flow.step = step
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                print(e)
                return False

    def get_flow_list(self):
        with self.Session() as session:
            try:
                flows = session.query(FlowBean).all()
                return [{
                    'id': item.id,
                    'description': item.description,
                    'step': item.step,
                } for item in flows]
            except Exception as e:
                session.rollback()
                print(e)
                return []

    def delete_by_id(self, id):
        with self.Session() as session:
            try:
                flow = session.query(FlowBean).filter_by(id=id).first()
                if flow:
                    session.delete(flow)
                    session.commit()
                    return True
            except Exception as e:
                session.rollback()
                print(e)
                return False

    def get_flow_by_id(self, id):
        with self.Session() as session:
            try:
                return session.query(FlowBean).filter_by(id=id).first()
            except Exception as e:
                session.rollback()
                print(e)
                return None
