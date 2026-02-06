from datetime import date, datetime

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from database import db
from models import MenuDay, MenuItem, Payment, MealOrder, DishFeedback
from utils.decorators import role_required
from wtf_forms.student_forms import PayForm, PreferencesForm, FeedbackForm, ReceiveMealForm


bp = Blueprint("student", __name__, url_prefix="/student")


@bp.get("/dashboard")
@login_required
@role_required("student")
def dashboard():
    today = date.today()
    orders = db.session.query(MealOrder).filter_by(student_id=current_user.id, day=today).all()
    return render_template("student/dashboard.html", orders=orders, today=today)


@bp.get("/menu")
@login_required
@role_required("student")
def menu():
    day_str = request.args.get("day")
    selected_day = date.fromisoformat(day_str) if day_str else date.today()

    menu_day = db.session.query(MenuDay).filter_by(day=selected_day).first()
    items = menu_day.items if menu_day else []
    return render_template("student/menu.html", items=items, selected_day=selected_day)


@bp.get("/pay")
@login_required
@role_required("student")
def pay_get():
    form = PayForm()
    return render_template("student/pay.html", form=form)


@bp.post("/pay")
@login_required
@role_required("student")
def pay_post():
    form = PayForm()
    if not form.validate_on_submit():
        return render_template("student/pay.html", form=form)

    payment_type = form.payment_type.data
    amount = int(form.amount_rub.data)

    payment = Payment(
        student_id=current_user.id,
        payment_type=payment_type,
        amount_rub=amount,
        status="paid",
    )
    db.session.add(payment)
    db.session.commit()

    flash("Оплата зарегистрирована (демо).", "success")
    return redirect(url_for("student.dashboard"))


@bp.get("/receive")
@login_required
@role_required("student")
def receive_get():
    form = ReceiveMealForm()
    return render_template("student/my_orders.html", form=form, today=date.today())


@bp.post("/receive")
@login_required
@role_required("student")
def receive_post():
    form = ReceiveMealForm()
    if not form.validate_on_submit():
        return render_template("student/my_orders.html", form=form, today=date.today())

    today = date.today()
    meal_type = form.meal_type.data

    order = db.session.query(MealOrder).filter_by(
        student_id=current_user.id, day=today, meal_type=meal_type
    ).first()

    if not order:
        order = MealOrder(student_id=current_user.id, day=today, meal_type=meal_type, paid=False)
        db.session.add(order)
        db.session.flush()

    if order.received_by_student_at:
        flash("Вы уже отмечали получение для этого приема пищи.", "warning")
        db.session.rollback()
        return redirect(url_for("student.dashboard"))

    order.received_by_student_at = datetime.utcnow()
    db.session.commit()

    flash("Отметка получения сохранена.", "success")
    return redirect(url_for("student.dashboard"))


@bp.get("/preferences")
@login_required
@role_required("student")
def preferences_get():
    form = PreferencesForm(
        allergies=current_user.allergies or "",
        preferences=current_user.preferences or "",
    )
    return render_template("student/preferences.html", form=form)


@bp.post("/preferences")
@login_required
@role_required("student")
def preferences_post():
    form = PreferencesForm()
    if not form.validate_on_submit():
        return render_template("student/preferences.html", form=form)

    current_user.allergies = form.allergies.data
    current_user.preferences = form.preferences.data
    db.session.commit()

    flash("Предпочтения сохранены.", "success")
    return redirect(url_for("student.dashboard"))


@bp.get("/feedback")
@login_required
@role_required("student")
def feedback_get():
    form = FeedbackForm()
    return render_template("student/feedback.html", form=form)


@bp.post("/feedback")
@login_required
@role_required("student")
def feedback_post():
    form = FeedbackForm()
    if not form.validate_on_submit():
        return render_template("student/feedback.html", form=form)

    fb = DishFeedback(
        student_id=current_user.id,
        dish_name=form.dish_name.data,
        rating=form.rating.data,
        comment=form.comment.data,
    )
    db.session.add(fb)
    db.session.commit()

    flash("Отзыв добавлен.", "success")
    return redirect(url_for("student.dashboard"))
