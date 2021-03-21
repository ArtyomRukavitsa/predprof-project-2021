from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectMultipleField, widgets, \
    IntegerField, PasswordField, DateField
from wtforms.validators import DataRequired, length


class AskDayForm(FlaskForm):
    day = DateField('День', format='%Y-%m-%d')
    city = StringField('Город', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


class LoginForm(FlaskForm):
    username = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')