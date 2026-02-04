import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp

CLASS_RE = r"^(?:[1-9]|1[0-1])\s?[А-ЯЁ]$"

PASS_RE = r"^(?=.*[A-Za-z])(?=.*\d).{8,}$"


class RegisterForm(FlaskForm):
    email = StringField(
        "Почта",
        validators=[
            DataRequired(),
            Email(),
            Length(max=254),
        ],
    )

    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(),
            Regexp(
                PASS_RE,
                message="Пароль должен быть минимум 8 символов и содержать хотя бы одну букву и одну цифру.",
            ),
        ],
    )

    school_class = StringField(
        "Класс",
        validators=[
            DataRequired(),
            Regexp(
                CLASS_RE,
                message="Класс должен быть в формате: 1-11 и буква А-Я (пример: 10А).",
            ),
        ],
    )

    submit = SubmitField("Зарегистрироваться")


class LoginForm(FlaskForm):
    email = StringField(
        "Почта",
        validators=[
            DataRequired(),
            Email(),
            Length(max=254),
        ],
    )

    password = PasswordField("Пароль", validators=[
        DataRequired(),
        Regexp(
                PASS_RE,
                message="Пароль должен быть минимум 8 символов и содержать хотя бы одну букву и одну цифру.",
            ),
        ])
    submit = SubmitField("Войти")