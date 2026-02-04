from flask import Blueprint, request, jsonify
from flask import render_template, redirect, url_for
from wtf_forms.auth import RegisterForm, LoginForm
from database import get_db_session
from models import User
from auth import hash_password, verify_password


main_page = Blueprint("main_page", __name__, url_prefix="/")


@main_page.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # тут создаёшь пользователя
        return redirect(url_for("main_page.index"))
    # если POST и есть ошибки — они окажутся в form.<field>.errors
    return render_template(
        "register.html",
        form=form,
        title="Регистрация",
        heading="Регистрация",
    )


@main_page.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # тут выдать JWT
        return redirect(url_for("main_page.index"))
    return render_template(
        "login.html",
        form=form,
        title="Вход",
        heading="Вход",
    )


@main_page.route("/", methods=["GET", "POST"])
def index():
    return "Асхаб чёрный"