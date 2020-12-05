import os
from flask import Flask, render_template, send_from_directory


app = Flask(__name__)


@app.route('/')
def main():
    return "здесь будет главная"


@app.route('/all')
def get_all():
    return "здесь будут преподаватели"


@app.route('/goals/<goal>/')
def get_goal(goal):
    return "здесь будет цель <goal>"


@app.route('/profiles/<profile_id>/')
def get_profile_by_id(profile_id):
    return "здесь будет преподаватель <profile_id>"


@app.route('/request/')
def get_request():
    return "здесь будет заявка на подбор"


@app.route('/request_done/')
def get_tour_by_id():
    return "заявка на подбор отправлена"


@app.route('/booking/<profile_id>/<day_of_week>/<time>/')
def get_tour_by_id(profile_id, day_of_week, time):
    return "здесь будет форма бронирования <profile_id>"


@app.route('/booking_done/')
def get_tour_by_id():
    return "заявка отправлена"


# https://flask.palletsprojects.com/en/1.1.x/patterns/favicon/
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run()
