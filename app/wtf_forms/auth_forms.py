from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6, max=128)])
    remember = BooleanField("Запомнить меня")


class RegisterForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6, max=128)])
    role = SelectField(
        "Роль",
        choices=[("student", "Ученик"), ("cook", "Повар"), ("admin", "Администратор")],
        default="student",
        validators=[DataRequired()],
    )
