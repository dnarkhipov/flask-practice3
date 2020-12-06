from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.fields.html5 import TelField


class BookingForm(FlaskForm):
    clientWeekday = HiddenField()
    clientTime = HiddenField()
    clientTeacher = HiddenField()

    clientName = StringField('Вас зовут')
    clientPhone = TelField('Ваш телефон')
