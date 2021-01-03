import json
from typing import Dict, List, Optional

from pathlib import Path

from .record_base import RecordBase
from .teacher import Teacher

data_path = Path(__file__).parent

GOALS_JSON = data_path.joinpath('goals.json')
TEACHERS_JSON = data_path.joinpath('teachers.json')
BOOKING_JSON = data_path.joinpath('booking.json')
REQUEST_JSON = data_path.joinpath('request.json')

REQUEST_TIME_LIMITS = {
    'limit1_2': '1-2 часа в неделю',
    'limit3_5': '3-5 часов в неделю',
    'limit5_7': '5-7 часов в неделю',
    'limit7_10': '7-10 часов в неделю'
}


class InternalDbError(Exception):
    pass


class MockDB:
    def __init__(self):
        self.time_limits = REQUEST_TIME_LIMITS
        try:
            with open(GOALS_JSON, 'r') as f:
                self.goals: Dict = json.load(f)

            with open(TEACHERS_JSON, 'r') as f:
                self.teachers: List = json.load(f)

            if not self.goals or len(self.goals) < 4 or not self.teachers or len(self.teachers) == 0:
                raise Exception

        except Exception:
            raise InternalDbError("Ошибка при инициализации БД. Необходимо выполнить экспорт данных в json командой python -m data")

    def search_teacher_by_id(self, teacher_id: int) -> Optional[Teacher]:
        profile = next((t for t in self.teachers if t['id'] == teacher_id), None)
        if profile is None:
            return None
        return Teacher(**profile)

    @staticmethod
    def _add_db_record(record: RecordBase, json_file: Path):
        """
        Сохраняем заявку в файл в JSON-формате
        :param record : заявка
        """
        if json_file.exists():
            """
            файл с заявками должен оставаться корректным по формату JSON,
            самое простое решение - перепистаь его заново с новой записью 
            """
            try:
                with open(json_file, 'r') as f:
                    records_list = json.load(f)
            except Exception as err:
                raise InternalDbError(str(err))
        else:
            records_list = []

        records_list.append(record.as_dict())

        try:
            with open(json_file, 'w', encoding='utf8') as f:
                json.dump(records_list, f, ensure_ascii=False)

        except Exception as err:
            raise InternalDbError(str(err))

    @staticmethod
    def add_booking_record(record: RecordBase):
        MockDB._add_db_record(record, BOOKING_JSON)

    @staticmethod
    def add_request_record(record: RecordBase):
        MockDB._add_db_record(record, REQUEST_JSON)


"""
Псевдо-БД для чтения данных из JSON файлов и сохранения заявок и бронирований
Перед использованием необходимо сгенерировать файлы из исходного файла data.py командой python -m data
"""
db = MockDB()
