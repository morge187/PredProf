from datetime import date, datetime

from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required

from database import db
from models import Payment, MealOrder, ProcurementRequest
from utils.decorators import role_required
from wtf_forms.admin_forms import DecideProcurementForm, ReportForm

import csv
import io


bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.get("/dashboard")
@login_required
@role_required("admin")
def dashboard():
    return render_template("admin/dashboard.html")


@bp.get("/stats")
@login_required
@role_required("admin")
def stats():
    day_str = request.args.get("day")
    selected_day = date.fromisoformat(day_str) if day_str else date.today()

    payments_sum = db.session.query(Payment).filter(
        Payment.created_at >= datetime.combine(selected_day, datetime.min.time()),
        Payment.created_at <= datetime.combine(selected_day, datetime.max.time()),
        Payment.status == "paid"
    ).with_entities(db.func.coalesce(db.func.sum(Payment.amount_rub), 0)).scalar()

    visits = db.session.query(MealOrder).filter(
        MealOrder.day == selected_day,
        MealOrder.issued_by_cook_at.isnot(None)
    ).count()

    return render_template("admin/stats.html", selected_day=selected_day, payments_sum=payments_sum, visits=visits)


@bp.get("/procurements")
@login_required
@role_required("admin")
def procurements():
    reqs = db.session.query(ProcurementRequest).order_by(ProcurementRequest.created_at.desc()).all()
    form = DecideProcurementForm()
    return render_template("admin/procurements.html", reqs=reqs, form=form)


@bp.post("/procurements/decide")
@login_required
@role_required("admin")
def procurements_decide():
    form = DecideProcurementForm()
    if not form.validate_on_submit():
        return redirect(url_for("admin.procurements"))

    req = db.session.get(ProcurementRequest, int(form.request_id.data))
    if not req:
        flash("Заявка не найдена.", "danger")
        return redirect(url_for("admin.procurements"))

    if req.status != "pending":
        flash("Заявка уже обработана ранее.", "warning")
        return redirect(url_for("admin.procurements"))

    req.status = form.decision.data
    req.comment = form.comment.data
    req.decided_at = datetime.utcnow()
    db.session.commit()

    flash("Решение сохранено.", "success")
    return redirect(url_for("admin.procurements"))


@bp.get("/report")
@login_required
@role_required("admin")
def report_get():
    form = ReportForm()
    return render_template("admin/report.html", form=form)


@bp.post("/report")
@login_required
@role_required("admin")
def report_post():
    form = ReportForm()
    if not form.validate_on_submit():
        return render_template("admin/report.html", form=form)

    start = form.start_date.data
    end = form.end_date.data

    payments = db.session.query(Payment).filter(
        Payment.created_at >= datetime.combine(start, datetime.min.time()),
        Payment.created_at <= datetime.combine(end, datetime.max.time()),
        Payment.status == "paid"
    ).all()

    orders = db.session.query(MealOrder).filter(
        MealOrder.day >= start,
        MealOrder.day <= end
    ).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Тип", "ID", "Дата/Время", "Сумма/Статус", "Ученик", "Дополнительно"])

    for p in payments:
        writer.writerow(["payment", p.id, p.created_at.isoformat(), p.amount_rub, p.student_id, p.payment_type])

    for o in orders:
        writer.writerow(["meal_order", o.id, o.day.isoformat(), "issued" if o.issued_by_cook_at else "not_issued",
                         o.student_id, o.meal_type])

    mem = io.BytesIO(output.getvalue().encode("utf-8"))
    return send_file(mem, mimetype="text/csv", as_attachment=True, download_name="report.csv")
