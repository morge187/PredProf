from datetime import date, datetime

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from database import db
from models import MealOrder, ProductStock, DishStock, ProcurementRequest, ProcurementItem
from utils.decorators import role_required
from wtf_forms.cook_forms import IssueMealForm, StockForm, ProcurementForm


bp = Blueprint("cook", __name__, url_prefix="/cook")


@bp.get("/dashboard")
@login_required
@role_required("cook")
def dashboard():
    today = date.today()
    issued = db.session.query(MealOrder).filter(
        MealOrder.day == today,
        MealOrder.issued_by_cook_at.isnot(None)
    ).count()
    return render_template("cook/dashboard.html", today=today, issued=issued)


@bp.get("/issue")
@login_required
@role_required("cook")
def issue_get():
    form = IssueMealForm()
    return render_template("cook/issue_meal.html", form=form)


@bp.post("/issue")
@login_required
@role_required("cook")
def issue_post():
    form = IssueMealForm()
    if not form.validate_on_submit():
        return render_template("cook/issue_meal.html", form=form)

    order = db.session.query(MealOrder).filter_by(
        student_id=form.student_id.data,
        day=date.today(),
        meal_type=form.meal_type.data
    ).first()

    if not order:
        flash("Заказ/отметка ученика не найдены на сегодня. Создайте сначала у ученика.", "warning")
        return redirect(url_for("cook.issue_get"))

    if order.issued_by_cook_at:
        flash("Выдача уже была учтена ранее.", "warning")
        return redirect(url_for("cook.issue_get"))

    order.issued_by_cook_at = datetime.utcnow()
    db.session.commit()

    flash("Выдача учтена.", "success")
    return redirect(url_for("cook.dashboard"))


@bp.get("/inventory")
@login_required
@role_required("cook")
def inventory_get():
    products = db.session.query(ProductStock).order_by(ProductStock.name).all()
    dishes = db.session.query(DishStock).order_by(DishStock.dish_name).all()
    form = StockForm()
    return render_template("cook/inventory.html", products=products, dishes=dishes, form=form)


@bp.post("/inventory")
@login_required
@role_required("cook")
def inventory_post():
    form = StockForm()
    if not form.validate_on_submit():
        return redirect(url_for("cook.inventory_get"))

    if form.kind.data == "product":
        item = db.session.query(ProductStock).filter_by(name=form.name.data).first()
        if not item:
            item = ProductStock(name=form.name.data, unit=form.unit.data, quantity=0)
            db.session.add(item)
        item.quantity = float(form.quantity.data)
        item.unit = form.unit.data
    else:
        item = db.session.query(DishStock).filter_by(dish_name=form.name.data).first()
        if not item:
            item = DishStock(dish_name=form.name.data, portions_available=0)
            db.session.add(item)
        item.portions_available = int(form.quantity.data)

    db.session.commit()
    flash("Остатки обновлены.", "success")
    return redirect(url_for("cook.inventory_get"))


@bp.get("/procurement/new")
@login_required
@role_required("cook")
def procurement_new_get():
    form = ProcurementForm()
    return render_template("cook/procurement_new.html", form=form)


@bp.post("/procurement/new")
@login_required
@role_required("cook")
def procurement_new_post():
    form = ProcurementForm()
    if not form.validate_on_submit():
        return render_template("cook/procurement_new.html", form=form)

    req = ProcurementRequest(created_by_cook_id=current_user.id, status="pending")
    db.session.add(req)
    db.session.flush()

    item = ProcurementItem(
        request_id=req.id,
        product_name=form.product_name.data,
        quantity=float(form.quantity.data),
        unit=form.unit.data,
    )
    db.session.add(item)
    db.session.commit()

    flash("Заявка на закупку создана.", "success")
    return redirect(url_for("cook.procurements"))


@bp.get("/procurements")
@login_required
@role_required("cook")
def procurements():
    reqs = db.session.query(ProcurementRequest).order_by(ProcurementRequest.created_at.desc()).all()
    return render_template("cook/procurements.html", reqs=reqs)
