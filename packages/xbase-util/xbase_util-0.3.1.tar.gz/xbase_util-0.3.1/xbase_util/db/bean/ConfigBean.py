from sqlalchemy import Column, Integer, String, TEXT, Boolean

from xbase_util.db.bean import DbBase


class ConfigBean(DbBase):
    __tablename__ = 'configs'
    id = Column(Integer, primary_key=True)
    description = Column(TEXT)

    label_all_true = Column(Boolean, nullable=False)
    label_is_output_unmatch = Column(Boolean, nullable=False)
    label_duration = Column(Integer, nullable=False)
    splitNumber = Column(Integer, nullable=False)

    mapping_le_path = Column(String, nullable=False)
    pcap_per_subsection = Column(Integer, nullable=False)
    pcap_process = Column(Integer, nullable=False)
    pcap_thread_in_process = Column(Integer, nullable=False)
    replace_source = Column(TEXT, nullable=False)  #用列表传
    replace_destination = Column(String, nullable=False)
    replace_mapping = Column(TEXT, nullable=False)  #用列表传
    replace_save_to = Column(String, nullable=False)

    session_all_true = Column(Boolean, nullable=False)
    session_start_time = Column(String, nullable=False)
    session_end_time = Column(String, nullable=False)
    session_expression = Column(String)
    session_alive = Column(String)
    catalogue = Column(String)
    session_size = Column(Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description or "",

            'label_all_true': self.label_all_true,
            'label_is_output_unmatch': self.label_is_output_unmatch,
            'label_duration': self.label_duration,
            'splitNumber': self.splitNumber,

            'mapping_le_path': self.mapping_le_path or "",

            'pcap_per_subsection': self.pcap_per_subsection,
            'pcap_process': self.pcap_process,
            'pcap_thread_in_process': self.pcap_thread_in_process,

            'replace_source': self.replace_source or "",
            'replace_destination': self.replace_destination or "",
            'replace_mapping': self.replace_mapping or "",
            'replace_save_to': self.replace_save_to or "",

            'session_all_true': self.session_all_true,
            'session_start_time': self.session_start_time or "",
            'session_end_time': self.session_end_time or "",
            'session_expression': self.session_expression or "",
            'session_alive': self.session_alive or "",
            'session_size': self.session_size or "",
            'catalogue': self.catalogue or "",
        }

    def to_session_dict(self):
        return {
            'id': self.id,
            'session_all_true': self.session_all_true,
            'session_start_time': self.session_start_time or "",
            'session_end_time': self.session_end_time or "",
            'session_expression': self.session_expression or "",
            'session_alive': self.session_alive or "",
            'session_size': self.session_size or "",
        }

    def to_pcap_dict(self):
        return {
            'id': self.id,
            'pcap_per_subsection': self.pcap_per_subsection,
            'pcap_process': self.pcap_process,
            'pcap_thread_in_process': self.pcap_thread_in_process,
        }

    def to_label_dict(self):
        return {
            'id': self.id,
            'label_all_true': self.label_all_true,
            'label_is_output_unmatch': self.label_is_output_unmatch,
            'label_duration': self.label_duration,
        }

    def to_mapping(self):
        return {
            'id': self.id,
            'mapping_le_path': self.mapping_le_path or "",
        }

    def to_replace(self):
        return {
            'id': self.id,
            'replace_source': self.replace_source or "",
            'replace_destination': self.replace_destination or "",
            'replace_mapping': self.replace_mapping or "",
            'replace_save_to': self.replace_save_to or "",
        }
