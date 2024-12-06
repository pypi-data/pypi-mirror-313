import traceback

from xbase_util.db.bean.ConfigBean import ConfigBean


class ConfigDao:
    def __init__(self,Session):
        self.Session = Session

    def add(self, id, description, label_all_true, label_is_output_unmatch,
            label_duration,
            mapping_le_path, pcap_per_subsection, pcap_process, pcap_thread_in_process,
            replace_source, replace_destination, replace_mapping, replace_save_to, session_all_true, session_start_time,
            session_end_time, session_expression, session_alive, session_size, splitNumber,catalogue
            ):
        with self.Session() as session:
            try:
                if id is None:
                    bean = ConfigBean(
                        description=description,
                        label_all_true=label_all_true,
                        label_is_output_unmatch=label_is_output_unmatch,
                        label_duration=label_duration,
                        mapping_le_path=mapping_le_path,
                        pcap_per_subsection=pcap_per_subsection,
                        pcap_process=pcap_process,
                        pcap_thread_in_process=pcap_thread_in_process,
                        replace_source=replace_source,
                        replace_destination=replace_destination,
                        replace_mapping=replace_mapping,
                        replace_save_to=replace_save_to,
                        session_all_true=session_all_true,
                        session_start_time=session_start_time,
                        session_end_time=session_end_time,
                        session_expression=session_expression,
                        session_alive=session_alive,
                        session_size=session_size,
                        splitNumber=splitNumber,
                        catalogue=catalogue
                    )
                    session.add(bean)
                    session.commit()
                    return True
                else:
                    config = session.query(ConfigBean).filter(ConfigBean.id == id).first()
                    if config is None:
                        return False
                    config.description = description
                    config.label_all_true = label_all_true
                    config.label_is_output_unmatch = label_is_output_unmatch
                    config.label_duration = label_duration
                    config.mapping_le_path = mapping_le_path
                    config.pcap_per_subsection = pcap_per_subsection
                    config.pcap_process = pcap_process
                    config.pcap_thread_in_process = pcap_thread_in_process
                    config.replace_source = replace_source
                    config.replace_destination = replace_destination
                    config.replace_mapping = replace_mapping
                    config.replace_save_to = replace_save_to
                    config.session_all_true = session_all_true
                    config.session_start_time = session_start_time
                    config.session_end_time = session_end_time
                    config.session_expression = session_expression
                    config.session_alive = session_alive
                    config.session_size = session_size
                    config.splitNumber = splitNumber
                    config.catalogue=catalogue
                    session.commit()
            except Exception as e:
                session.rollback()
                traceback.print_exc()
                print(e)

    def get_config_file_list(self):
        with self.Session() as session:
            try:
                config_list = session.query(ConfigBean).all()
                return [d.to_dict() for d in config_list]
            except Exception as e:
                session.rollback()
                print(e)

    def remove_by_id(self, id):
        with self.Session() as session:
            try:
                session.query(ConfigBean).filter(ConfigBean.id == id).delete()
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)

    def get_config_by_id(self, id):
        with self.Session() as session:
            try:
                return session.query(ConfigBean).filter(ConfigBean.id == id).first()
            except Exception as e:
                session.rollback()
                print(e)

    def set_config_session_by_id(self, id, session_all_true, session_start_time, session_end_time, session_expression,
                                 session_alive, session_size):
        with self.Session() as session:
            try:
                config = session.query(ConfigBean).filter(ConfigBean.id == id).first()
                config.session_all_true = session_all_true
                config.session_start_time = session_start_time
                config.session_end_time = session_end_time
                config.session_expression = session_expression
                config.session_alive = session_alive
                config.session_size = session_size
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)

    def set_config_pcap_by_id(self, id,
                              pcap_per_subsection,
                              pcap_process,
                              pcap_thread_in_process):
        with self.Session() as session:
            try:
                config = session.query(ConfigBean).filter(ConfigBean.id == id).first()
                config.pcap_per_subsection = pcap_per_subsection
                config.pcap_process = pcap_process
                config.pcap_thread_in_process = pcap_thread_in_process
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)

    def set_config_label_by_id(self, id,
                               label_all_true,
                               label_is_output_unmatch,
                               label_duration):
        with self.Session() as session:
            try:
                config = session.query(ConfigBean).filter(ConfigBean.id == id).first()
                config.label_all_true = label_all_true
                config.label_is_output_unmatch = label_is_output_unmatch
                config.label_duration = label_duration
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)

    def set_config_mapping_by_id(self, id, mapping_le_path):
        with self.Session() as session:
            try:
                config = session.query(ConfigBean).filter(ConfigBean.id == id).first()
                config.mapping_le_path = mapping_le_path
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)

    def set_config_replace_by_id(self, id, replace_source, replace_destination, replace_mapping, replace_save_to):
        with self.Session() as session:
            try:
                config = session.query(ConfigBean).filter(ConfigBean.id == id).first()
                config.replace_source = replace_source
                config.replace_destination = replace_destination
                config.replace_mapping = replace_mapping
                config.replace_save_to = replace_save_to
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
# 修改脚本带redis获取状态
# 提异常，正常dns和异常都要，要新的黑白样本
# app
# capture
# 日报规范问题 [做了什么][完成的进度][遇到的问题][问题研究的进度和方案]
