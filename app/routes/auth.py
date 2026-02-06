from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required

from database import db
from models import User
from utils.security import hash_password, verify_password
from wtf_forms.auth_forms import LoginForm, RegisterForm


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.get("/login")
@bp.post("/login")
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=form.username.data).first()

        if not user or not verify_password(form.password.data, user.password_hash):
            flash("Неверный логин или пароль.", "danger")
            return render_template("auth/login.html", form=form)

        login_user(user, remember=form.remember.data)

        next_url = request.args.get("next")
        if next_url:
            return redirect(next_url)

        # Фолбэк: отправляем по роли в кабинет
        if user.role == "student":
            return redirect(url_for("student.dashboard"))
        if user.role == "cook":
            return redirect(url_for("cook.dashboard"))
        if user.role == "admin":
            return redirect(url_for("admin.dashboard"))

        # Если роль неожиданная
        return redirect(url_for("auth.login"))

    return render_template("auth/login.html", form=form)


@bp.get("/register")
@bp.post("/register")
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if db.session.query(User).filter_by(username=form.username.data).first():
            flash("Такой логин уже занят.", "warning")
            return render_template("auth/register.html", form=form)

        if db.session.query(User).filter_by(email=form.email.data).first():
            flash("Такой email уже зарегистрирован.", "warning")
            return render_template("auth/register.html", form=form)

        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hash_password(form.password.data),
            role=form.role.data,
        )

        db.session.add(user)
        db.session.commit()

        flash("Регистрация успешна. Теперь войдите.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@bp.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
