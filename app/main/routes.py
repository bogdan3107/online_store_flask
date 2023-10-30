from flask import render_template, current_app, json, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.models import Product, User, Order
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


@bp.route('/customer/<username>', methods=['GET', 'POST'])
@login_required
def load_customer(username):
    customer = User.query.filter_by(username=username).first_or_404()

    return render_template('customer.html', customer=customer)
     

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

    return jsonify({'message': 'Product removed from the cart'})
    
    

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