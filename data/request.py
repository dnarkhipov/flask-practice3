from .record_base import dataclass, RecordBase


@dataclass
class RequestRecord(RecordBase):
    goal: str = ''
    time_limit: str = ''
    client_name: str = ''
    client_phone: str = ''
