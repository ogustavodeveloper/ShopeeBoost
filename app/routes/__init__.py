from flask import Blueprint

main_bp = Blueprint('main', __name__)
features_bp = Blueprint('features', __name__)

from app.routes import main, features