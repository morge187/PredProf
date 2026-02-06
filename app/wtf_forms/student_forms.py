from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, IntegerField, StringField
from wtforms.validators import DataRequired, NumberRange, Length


class PayForm(FlaskForm):
    payment_type = SelectField(
        "Тип оплаты",
        choices=[("single", "Разовый платеж"), ("subscription", "Абонемент")],
        validators=[DataRequired()],
    )
    amount_rub = IntegerField("Сумма (руб.)", validators=[DataRequired(), NumberRange(min=1, max=5000)])


class ReceiveMealForm(FlaskForm):
    meal_type = SelectField(
        "Прием пищи",
        choices=[("breakfast", "Завтрак"), ("lunch", "Обед")],
        validators=[DataRequired()],
    )


class PreferencesForm(FlaskForm):
    allergies = TextAreaField("Аллергии (через запятую)", validators=[Length(max=500)])
    preferences = TextAreaField("Предпочтения/ограничения", validators=[Length(max=500)])


class FeedbackForm(FlaskForm):
    dish_name = StringField("Блюдо", validators=[DataRequired(), Length(max=120)])
    rating = IntegerField("Оценка (1-5)", validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField("Комментарий", validators=[Length(max=2000)])
