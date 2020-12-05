import os
from flask import Flask, render_template, send_from_directory, redirect
from flask_wtf.csrf import CSRFProtect
from data import MockDB

from profile import Profile


day_names_ru = {
    "mon": {"short": "Пн", "full": "Понедельник"},
    "tue": {"short": "Вт", "full": "Вторник"},
    "wed": {"short": "Ср", "full": "Среда"},
    "thu": {"short": "Чт", "full": "Четверг"},
    "fri": {"short": "Пт", "full": "Пятница"},
    "sat": {"short": "Сб", "full": "Суббота"},
    "sun": {"short": "Вс", "full": "Воскресенье"}
}

app = Flask(__name__)

csrf = CSRFProtect(app)
SECRET_KEY = os.urandom(43)
app.config['SECRET_KEY'] = SECRET_KEY


base_template_attr = {
    """
    Базовые настроки макета (название сайта, пунктов меню и т.п.)
    """
    "title": "TINYSTEPS",
    "nav_title": "TINYSTEPS",
    "nav_items": {
        "/all": "Все репетиторы",
        "/request/": "Заявка на подбор",
    }
}


"""
Псевдо-БД для чтения данных из JSON файлов
Перед использованием необходимо сгенерировать файлы из исходного файла data.py командой python -m data
"""
db = MockDB()


@app.route('/')
def main():
    # return "здесь будет главная"
    return render_template(
        'index.html',
        **base_template_attr
    )


@app.route('/all')
def get_all():
    return "здесь будут преподаватели"


@app.route('/goals/<goal>/')
def get_goal(goal):
    return "здесь будет цель <goal>"


@app.route('/profiles/<int:profile_id>/')
def get_profile_by_id(profile_id: int):
    # return "здесь будет преподаватель <profile_id>"
    profile = db.search_teacher_by_id(profile_id)
    if not profile:
        return redirect('/all')

    return render_template(
        'profile.html',
        **base_template_attr,
        profile=Profile(**profile),
        day_names=day_names_ru
    )


@app.route('/request/')
def get_request():
    return "здесь будет заявка на подбор"


@app.route('/request_done/')
def get_request_done():
    return "заявка на подбор отправлена"


@app.route('/booking/<int:profile_id>/<day_of_week>/<time>/')
def get_booking_form(profile_id: int, day_of_week, time):
    return "здесь будет форма бронирования <profile_id>"


@app.route('/booking_done/')
def get_booking_form_done():
    return "заявка отправлена"


# https://flask.palletsprojects.com/en/1.1.x/patterns/favicon/
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run()
