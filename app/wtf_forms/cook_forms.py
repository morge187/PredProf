from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, FloatField
from wtforms.validators import DataRequired, NumberRange, Length


class IssueMealForm(FlaskForm):
    student_id = IntegerField("ID ученика", validators=[DataRequired(), NumberRange(min=1)])
    meal_type = SelectField(
        "Прием пищи",
        choices=[("breakfast", "Завтрак"), ("lunch", "Обед")],
        validators=[DataRequired()],
    )


class StockForm(FlaskForm):
    kind = SelectField("Тип", choices=[("product", "Продукт"), ("dish", "Готовое блюдо")], validators=[DataRequired()])
    name = StringField("Название", validators=[DataRequired(), Length(max=120)])
    quantity = FloatField("Количество/порции", validators=[DataRequired(), NumberRange(min=0)])
    unit = SelectField("Ед.", choices=[("kg", "кг"), ("l", "л"), ("pcs", "шт")], default="kg")


class ProcurementForm(FlaskForm):
    product_name = StringField("Продукт", validators=[DataRequired(), Length(max=120)])
    quantity = FloatField("Количество", validators=[DataRequired(), NumberRange(min=0.01)])
    unit = SelectField("Ед.", choices=[("kg", "кг"), ("l", "л"), ("pcs", "шт")], default="kg")
