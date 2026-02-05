from flask import Blueprint, jsonify, render_template, redirect, url_for, request, make_response
from wtf_forms.auth import RegisterForm, LoginForm
from database import get_db_session
from utils.error import UserError

from services.user_service import UserService
from utils.jwt_utils import create_access_token


main_page = Blueprint("main_page", __name__, url_prefix="/")


@main_page.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        with get_db_session() as db:
            try:
                user = UserService.create_user(
                    db,
                    {
                        "email": form.email.data,
                        "password": form.password.data,
                        "class_name": form.school_class.data
                    },
                )
            except UserError as e:
                if hasattr(form, e.field):
                    getattr(form, e.field).errors.append(e.cause)
                else:
                    form.errors[e.field] = form.errors.get(e.field, []) + [e.cause]
                return render_template(
                    "register.html",
                    form=form,
                    title="Регистрация",
                    heading="Регистрация",
                )

            token, expires_in = create_access_token(user_id=str(user.id), role=str(user.role))
            
            response = make_response(render_template("index.html", user=user, success="register"))
            response.headers['X-Auth-Token'] = token
            response.set_cookie('auth_token', token, max_age=expires_in)
            return response

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
        with get_db_session() as db:
            try:
                user = UserService.authenticate_user(
                    db,
                    form.email.data,
                    form.password.data
                )
            except UserError as e:
                if hasattr(form, e.field):
                    getattr(form, e.field).errors.append(e.cause)
                else:
                    form.errors[e.field] = form.errors.get(e.field, []) + [e.cause]
                return render_template(
                    "login.html",
                    form=form,
                    title="Вход",
                    heading="Вход",
                    error=str(e.cause),
                )

            token, expires_in = create_access_token(user_id=str(user.id), role=str(user.role))
            
            response = make_response(render_template("index.html", user=user, success="login"))
            response.headers['X-Auth-Token'] = token
            response.set_cookie('auth_token', token, max_age=expires_in)
            return response
    
    return render_template(
        "login.html",
        form=form,
        title="Вход",
        heading="Вход",
    )


@main_page.route("/", methods=["GET"])
def index():
    return "Acхаб чёрный"
