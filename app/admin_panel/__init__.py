from flask import Blueprint

bp = Blueprint('admin_panel_bp', __name__)

from app.admin_panel import routes