from . import bp
from flask import render_template, current_app, flash, redirect, url_for
from flask_admin.contrib.sqla import ModelView
from app.admin_panel.forms import AddProductForm
from app.models import Product, Category
from app import db
from werkzeug.utils import secure_filename
import os

class ProductsAdminView(ModelView):
    column_display_pk = True
    column_editable_list = ['name', 'description', 'price', 'stock', 'category']
    can_delete = True

class CategoryAdminView(ModelView):
    column_display_pk =True
    form_columns = ['name']
    can_delete = False

class UserAdminView(ModelView):
    column_display_pk =True
    column_exclude_list = ['password_hash']

class OrderItemAdminView(ModelView):
    column_display_pk =True



"""
@bp.route('/admin')
def admin():
    return render_template('admin_panel/admin_panel.html')
"""


@bp.route('/admin/create_product', methods=['GET', 'POST'])
def create_product():
    form = AddProductForm()
    if form.validate_on_submit():
        category_id = form.category.data
        category = Category.query.get(category_id)

        if not  category:
            return render_template('admin_panel/create_product.html', form=form)
        
        try:
            product = Product(
                name = form.name.data,
                description = form.description.data,
                price = form.price.data,
                stock = form.stock.data,
                category = [category],
                image_path = None
            )
            db.session.add(product)
        
            image = form.image.data
            filename = secure_filename(image.filename)
            filename_only = os.path.basename(filename)
            filepath = os.path.join(current_app.config['PRODUCT_IMAGE_DIR'], filename_only)
            image.save(filepath)
            product.image_path = os.path.relpath(filepath, current_app.static_folder)
            
            db.session.commit()

            flash('Product successfully created!', 'success')
            return redirect(url_for('admin.index'))
        except Exception as e:
            flash(f'Error creating product:{str(e)}', 'error')
    return render_template('admin_panel/create_product.html', form=form)
    
        
