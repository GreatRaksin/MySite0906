from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length

from habrClone.models import User


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя/Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    password = StringField(validators=[DataRequired()])
    password2 = StringField(validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Используйте другое имя!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Используйте другой Email!')


class AccountUpdateForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    picture = FileField(validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Обновить')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Используйте другое имя!')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Используйте другой Email!')


class NewsForm(FlaskForm):
    body = TextAreaField('Текст новости:', validators=[DataRequired(), Length(min=1, max=200)])
    submit = SubmitField('Отправить')


class ZvonokForm(FlaskForm):
    phone = StringField('Ваш номер телефона:', validators=[DataRequired(), Length(9, 11)])
    body = TextAreaField('Текст новости:', validators=[DataRequired(), Length(min=1, max=200)])
    submit = SubmitField('Отправить')
