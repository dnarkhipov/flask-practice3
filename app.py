import os
import json
import random

from base64 import urlsafe_b64encode, urlsafe_b64decode

from flask import Flask, render_template, send_from_directory, redirect, url_for, request
from flask_wtf.csrf import CSRFProtect

from data import db
from profile import Profile
from booking_form import BookingForm
from request_form import RequestForm


weekday_names_ru = {
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


@app.route('/')
def main():
    # return "здесь будет главная"
    return render_template(
        'index.html',
        **base_template_attr,
        goals=db.goals,
        teachers=random.sample(db.teachers, 6)
    )


@app.route('/all')
def get_all():
    return "здесь будут преподаватели"


@app.route('/goals/<goal>/')
def get_goal(goal):
    # return "здесь будет цель <goal>"

    return render_template(
        'goal.html',
        **base_template_attr,
        goal_code=goal,
        goal_name=db.goals.get(goal, 'неопределенного направления'),
        teachers=sorted([t for t in db.teachers if goal in t.get('goals', [])], key=lambda t: t['rating'], reverse=True)
    )


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
        weekday_names=weekday_names_ru
    )


@app.route('/request/', methods=['GET', 'POST'])
def get_request():
    # return "здесь будет заявка на подбор"

    request_form = RequestForm()

    if request.method == 'POST' and request_form.validate():
        request_record = request_form.data
        # сохраняем данные формы без CSRF токена
        request_record.pop('csrf_token', None)
        db.add_request_record(request_record)

        # пакуем данные формы для передачи в квитанцию
        fdata = urlsafe_b64encode(bytes(json.dumps(request_record, ensure_ascii=False), 'utf-8'))
        return redirect(url_for('get_request_done', fdata=fdata))

    return render_template(
        'request.html',
        **base_template_attr,
        form=request_form
    )


@app.route('/request_done/<fdata>')
def get_request_done(fdata):
    # return "заявка на подбор отправлена"

    # распаковываем данные формы
    request_record = json.loads(urlsafe_b64decode(fdata).decode('utf-8'))
    return render_template(
        'request_done.html',
        **base_template_attr,
        request_info=request_record,
        goals=db.goals,
        time_limits=db.time_limits
    )


@app.route('/booking/<int:profile_id>/<day_of_week>/<time>/', methods=['GET', 'POST'])
def get_booking_form(profile_id: int, day_of_week, time):
    # return "здесь будет форма бронирования <profile_id>"

    profile = db.search_teacher_by_id(profile_id)
    if not profile:
        return redirect('/all')

    booking_form = BookingForm()
    booking_form.clientTeacher.data = profile_id
    booking_form.clientWeekday.data = day_of_week
    booking_form.clientTime.data = f'{time[:2]}:{time[-2:]}'

    if request.method == 'POST' and booking_form.validate():
        booking_record = booking_form.data
        # сохраняем данные формы без CSRF токена
        booking_record.pop('csrf_token', None)
        db.add_booking_record(booking_record)

        # пакуем данные формы для передачи в квитанцию
        fdata = urlsafe_b64encode(bytes(json.dumps(booking_record, ensure_ascii=False), 'utf-8'))
        return redirect(url_for('get_booking_form_done', fdata=fdata))

    return render_template(
        'booking.html',
        **base_template_attr,
        profile=Profile(**profile),
        form=booking_form,
        weekday_names=weekday_names_ru
    )


@app.route('/booking_done/<fdata>')
def get_booking_form_done(fdata):
    # return "заявка отправлена"

    # распаковываем данные формы
    booking_record = json.loads(urlsafe_b64decode(fdata).decode('utf-8'))
    return render_template(
        'booking_done.html',
        **base_template_attr,
        booking_info=booking_record,
        weekday_names=weekday_names_ru
    )


# https://flask.palletsprojects.com/en/1.1.x/patterns/favicon/
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run()
