from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, DateField
from wtforms.validators import DataRequired, NumberRange, Optional, Length


class DecideProcurementForm(FlaskForm):
    request_id = IntegerField("ID заявки", validators=[DataRequired(), NumberRange(min=1)])
    decision = SelectField("Решение", choices=[("approved", "Согласовать"), ("rejected", "Отклонить")], validators=[DataRequired()])
    comment = StringField("Комментарий", validators=[Optional(), Length(max=255)])


class ReportForm(FlaskForm):
    start_date = DateField("Начало", validators=[DataRequired()])
    end_date = DateField("Конец", validators=[DataRequired()])
