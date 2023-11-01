from flask import render_template, current_app, json, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.models import Product, User, Order
from app.main.forms import EditProfileForm
import json

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('products.html')

@bp.route('/products', methods=['GET', 'POST'])
def products():
    products = Product.query.all()
    #csrf_token = csrf._get_csrf_token()

    return render_template('products.html', title=('Products'), products=products)

@bp.route('/products/<id>', methods=['GET', 'POST'])
def load_product(id):
    product = Product.query.filter_by(id=id).first_or_404()
    return render_template('product.html', product=product)

@bp.route('/customer/<username>', methods=['GET', 'POST'])
@login_required
def load_customer(username):
    customer = User.query.filter_by(username=username).first_or_404()

    return render_template('customer.html', customer=customer)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.delivery_address = form.delivery_address.data
        current_user.phone_number = form.phone_number.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.load_customer', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.delivery_address.data = current_user.delivery_address
        form.phone_number.data = current_user.phone_number
    return render_template('edit_profile.html', title=('Edit Profile'),
                           form=form)
     
@bp.route('/shopping_cart', methods=['GET','POST'])
@login_required
def shopping_cart():
    cart_items = Order.query.filter_by(customer=current_user, status='cart')
    total_to_pay = 0
    for item in cart_items:
        total_to_pay += item.product.price * item.quantity
    return render_template('shopping_cart.html', cart_items=cart_items, total_to_pay=total_to_pay, title='Your cart')
    
@bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if current_user.is_anonymous:
        return jsonify({'message': 'You have to sign in to add a product to the cart!'}), 401

    data = request.get_json()
    product_id = data.get('product_id')

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found!'}), 404
    
    in_cart = Order.query.filter_by(product=product, customer=current_user, status='cart').first()
    if in_cart:
        in_cart.quantity += 1
    else:
        cart = Order(product=product, quantity=1, customer=current_user)
        db.session.add(cart)

    db.session.commit()
    
    return jsonify({'message': 'Product added to the cart'})

@bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if current_user.is_anonymous:
        return jsonify({'message': 'You are not permitted for this action!'}), 401
    
    data = request.get_json()
    product_id = data.get('product_id')

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found!'}), 404
    
    in_cart = Order.query.filter_by(product=product, customer=current_user, status='cart').first()
    if in_cart.quantity >= 1:
        db.session.delete(in_cart)    
        db.session.commit()

    cart_items = Order.query.filter_by(customer=current_user, status='cart').all()
    item_counts = {str(item.product_id): item.quantity for item in cart_items}
    
    return jsonify({'message': 'Product removed from the cart', 'item_counts': item_counts})

@bp.route('/update_quantity', methods=['POST'])
def update_quantity():
    if current_user.is_anonymous:
        return jsonify({'message': 'You are not permitted for this action!'}), 401

    data = request.get_json()
    product_id = data.get('product_id')
    action = data.get('action')  # 'increase' or 'decrease'

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    in_cart = Order.query.filter_by(product=product, customer=current_user, status='cart').first()
    if not in_cart:
        return jsonify({'message': 'Product not in cart'}), 404
    
    if action == 'increase':
        in_cart.quantity += 1
    elif action == 'decrease':
        if in_cart.quantity > 1:
            in_cart.quantity -= 1
        else:
            db.session.delete(in_cart)
    
    db.session.commit()

    cart_items = Order.query.filter_by(customer=current_user, status='cart').all()
    item_counts = {str(item.product_id): item.quantity for item in cart_items}

    return jsonify({'item_counts': item_counts})




@bp.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    pass

@bp.route('/shopping_temp_cart', methods=['GET'])
def shopping_temp_cart():
    try:
        products = Product.query.all()
        product_by_id = {product.id: product for product in products}

        # Получаем temp_cart из localStorage
        temp_cart_str = request.get_json().get('temp_cart')
        temp_cart = json.loads(temp_cart_str) if temp_cart_str else {}

        print(temp_cart_str)
        print(temp_cart)
        print(product_by_id)

    except json.JSONDecodeError:
        print('Error decoding the shopping cart data.', 'error')
        return redirect(url_for('main.index'))

    return render_template('shopping_temp_cart.html', title='Shopping cart', temp_cart=temp_cart, product_by_id=product_by_id)

@bp.route('/search', methods=['POST'])
def search():
    pass