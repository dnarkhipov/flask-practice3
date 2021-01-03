from .record_base import dataclass, RecordBase


@dataclass
class BookingRecord(RecordBase):
    client_weekday: str = ''
    client_time: str = ''
    client_teacher: str = ''
    client_name: str = ''
    client_phone: str = ''
