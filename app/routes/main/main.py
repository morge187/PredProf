from flask import Blueprint, request, jsonify
from database import get_db_session
from models import User
from auth import hash_password, verify_password


main_page = Blueprint("main_page", __name__, url_prefix="/")