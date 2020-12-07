from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms import validators
from wtforms.fields.html5 import TelField


class BookingForm(FlaskForm):
    clientWeekday = HiddenField()
    clientTime = HiddenField()
    clientTeacher = HiddenField()

    clientName = StringField('Вас зовут', [validators.InputRequired('Необходимо заполнить это поле')])
    clientPhone = TelField('Ваш телефон (11 цифр)', [
        validators.Regexp(
            r'^(\+7|8)[\s,(]?\d{3}[\s,)]?\d{3}[\s]?\d{2}[\s]?\d{2}$',
            message='Введите номер телефона в формате 11 цифр, например 89001234567'
        )
    ])
