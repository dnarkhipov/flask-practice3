import json
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Dict, List, Optional

from pathlib import Path


data_path = Path(__file__).parent

GOALS_JSON = data_path.joinpath('goals.json')
TEACHERS_JSON = data_path.joinpath('teachers.json')
BOOKING_JSON = data_path.joinpath('booking.json')


class MockDB:
    def __init__(self):
        try:
            with open(GOALS_JSON, 'r') as f:
                self._goals: 'Dict' = json.load(f)

            with open(TEACHERS_JSON, 'r') as f:
                self._teachers: 'List' = json.load(f)

            if not self._goals or len(self._goals) != 4 or not self._teachers or len(self._teachers) == 0:
                raise Exception

        except Exception:
            raise Exception("Ошибка при инициализации БД. Необходимо выполнить экспорт данных в json командой python -m data")

    @property
    def goals(self) -> 'Dict':
        return self._goals

    @property
    def teachers(self) -> 'List':
        return self._teachers

    def search_teacher_by_id(self, teacher_id: int) ->'Optional[Dict]':
        return next((t for t in self.teachers if t['id'] == teacher_id), None)

    @staticmethod
    def add_booking_record(booking: 'Dict'):
        """
        Сохраняем заявку на бронирование в файл в JSON-формате
        :param booking: заявка на бронирование
        """
        if BOOKING_JSON.exists():
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


__all__ = [
    'MockDB'
]
