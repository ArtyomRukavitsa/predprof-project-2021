from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectMultipleField, widgets, \
    IntegerField, PasswordField, DateField
from wtforms.validators import DataRequired, length


class AskDayForm(FlaskForm):
    day = DateField('Введите дату (формат: ГГГГ-ММ-ДД)', format='%Y-%m-%d')
    city = StringField('Город', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


class AskWeekForm(FlaskForm):
    day = DateField('Введите дату первого дня недели (формат: ГГГГ-ММ-ДД)', format='%Y-%m-%d')
    city = StringField('Город', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


class AskMonthForm(FlaskForm):
    month = StringField('Введите название месяца', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


class LoginForm(FlaskForm):
    username = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')