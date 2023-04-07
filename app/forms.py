from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
import wtforms as wf
from werkzeug.utils import secure_filename

from . import app
from .models import Position, Employee, User



def position_choices():
    choices = []
    with app.app_context():
        positions = Position.query.all()
        for position in positions:
            choices.append((position.id, position.name))
    return choices

class PositionForm(FlaskForm):
    name = wf.StringField(label='Введите должность', validators=[
        wf.validators.DataRequired()
    ])
    department = wf.StringField(label='Введите название отдела', validators=[
        wf.validators.DataRequired()
    ])
    wage = wf.IntegerField(label='Заработная плата', validators=[
        wf.validators.DataRequired()
    ])


    def validate(self, *args, **kwargs):
        if not super().validate():
            return False
        if self.wage.data < 0:
            self.wage.errors.append('Заработная плата не должно быть отрицательным')
            return False
        return True

class EmployeeForm(FlaskForm):
    name = wf.StringField(label='ФИО клиента', validators=[
        wf.validators.DataRequired()
    ])
    inn = wf.StringField(label='ИНН клиента', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(14)
    ])
    position_id = wf.SelectField(label='Должность', choices=position_choices,
                                 validators=[wf.validators.DataRequired(), ])


    def validate_inn(self, field):
        if Employee.query.filter_by(inn=field.data).count() > 0:
            raise wf.ValidationError('Сотрудник с данным инн уже существует')
        if not field.data[0] != '1' and not field.data[0] !='2':
            raise wf.ValidationError('inn должно начинаться на числа 1 или 2')


class PositionUpdateForm(FlaskForm):
    name = wf.StringField(label='Введите должность', validators=[
        wf.validators.DataRequired()
    ])
    department = wf.StringField(label='Введите название отдела', validators=[
        wf.validators.DataRequired()
    ])
    wage = wf.IntegerField(label='Заработная плата', validators=[
        wf.validators.DataRequired()
    ])


class EmployeeUpdateForm(FlaskForm):
    name = wf.StringField(label='ФИО клиента', validators=[
        wf.validators.DataRequired()
    ])
    inn = wf.StringField(label='ИНН клиента', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(14)
    ])
    position_id = wf.SelectField(label='Должность', choices=position_choices,
                                 validators=[wf.validators.DataRequired(), ])

class UserLoginForm(FlaskForm):
    username = wf.StringField(label='Логин', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(min=3, max=20)
    ])
    password = wf.PasswordField(label='Пароль', validators=[
        wf.validators.DataRequired()
    ])

    def validate_password(self, field):
        if len(field.data) < 8:
            raise wf.ValidationError('Длина пароля должнв быть минимум 8 символов')


class UserRegisterForm(UserLoginForm):
    password_2 = wf.PasswordField(label='Пароль', validators=[
        wf.validators.DataRequired()
    ])

    def validate(self, *args, **kwargs):
        if not super().validate(*args, **kwargs):
            return False
        if self.password.data != self.password_2.data:
            self.password_2.errors.append('Пароли должны совпадать')
            return False
        return True


