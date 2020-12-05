import json
from .data import goals, teachers
from . import GOALS_JSON, TEACHERS_JSON


def export_data():
    with open(GOALS_JSON, 'w', encoding='utf8') as f:
        json.dump(goals, f, ensure_ascii=False)
        print(f'Goals data save as {GOALS_JSON}')

    with open(TEACHERS_JSON, 'w', encoding='utf8') as f:
        json.dump(teachers, f, ensure_ascii=False)
        print(f'Teachers data save as {TEACHERS_JSON}')


if __name__ == '__main__':
    export_data()
