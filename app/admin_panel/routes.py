from . import bp
from flask import render_template
from flask_admin.contrib.sqla import ModelView
from app import db, admin
from app.models import Products


class ProductsAdminView(ModelView):
    column_display_pk = True
    form_columns = ['name', 'description', 'image_path']
    can_delete = False



@bp.route('/admin')
def admin():
    return render_template('admin_panel/admin.html')