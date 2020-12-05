from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Dict, List, Optional

import json


GOALS_JSON = 'goals.json'
TEACHERS_JSON = 'teachers.json'


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


__all__ = [
    'MockDB'
]
