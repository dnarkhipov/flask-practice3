import json
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Dict, List, Optional

from pathlib import Path


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

class MockDB:
    def __init__(self):
        self._time_limits = REQUEST_TIME_LIMITS
        try:
            with open(GOALS_JSON, 'r') as f:
                self._goals: 'Dict' = json.load(f)

            with open(TEACHERS_JSON, 'r') as f:
                self._teachers: 'List' = json.load(f)

            if not self._goals or len(self._goals) < 4 or not self._teachers or len(self._teachers) == 0:
                raise Exception

        except Exception:
            raise Exception("Ошибка при инициализации БД. Необходимо выполнить экспорт данных в json командой python -m data")

    @property
    def time_limits(self) -> 'Dict':
        return self._time_limits

    @property
    def goals(self) -> 'Dict':
        return self._goals

    @property
    def teachers(self) -> 'List':
        return self._teachers

    def search_teacher_by_id(self, teacher_id: int) -> 'Optional[Dict]':
        return next((t for t in self.teachers if t['id'] == teacher_id), None)

    @staticmethod
    def add_booking_record(booking: 'Dict'):
        """
        Сохраняем заявку на бронирование в файл в JSON-формате
        :param booking: заявка на бронирование
        """
        if BOOKING_JSON.exists():
            """
            файл с заявками должен оставаться корректным по формату JSON,
            самое простое решение - перепистаь его заново с новой записью 
            """
            try:
                with open(BOOKING_JSON, 'r') as f:
                    booking_list = json.load(f)
            except Exception:
                return
        else:
            booking_list = []

        booking_list.append(booking)

        try:
            with open(BOOKING_JSON, 'w', encoding='utf8') as f:
                json.dump(booking_list, f, ensure_ascii=False)

        except Exception:
            pass

    @staticmethod
    def add_request_record(request: 'Dict'):
        """
        Сохраняем заявку на подбор в файл в JSON-формате
        :param request: заявка на подбор
        """
        if REQUEST_JSON.exists():
            """
            файл с заявками должен оставаться корректным по формату JSON,
            самое простое решение - перепистаь его заново с новой записью 
            """
            try:
                with open(REQUEST_JSON, 'r') as f:
                    request_list = json.load(f)
            except Exception:
                return
        else:
            request_list = []

        request_list.append(request)

        try:
            with open(REQUEST_JSON, 'w', encoding='utf8') as f:
                json.dump(request_list, f, ensure_ascii=False)

        except Exception:
            pass


"""
Псевдо-БД для чтения данных из JSON файлов и сохранения заявок и бронирований
Перед использованием необходимо сгенерировать файлы из исходного файла data.py командой python -m data
"""
db = MockDB()


__all__ = [
    'db'
]
