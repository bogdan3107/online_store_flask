from flask import render_template, redirect, url_for, flash, request, jsonify, g, current_app
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.models import Product, User, Order, OrderItem
from app.main.forms import EditProfileForm, SearchForm, CheckoutForm

@bp.before_app_request
def before_request():
    g.search_form = SearchForm()

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
    cart_items = OrderItem.query.filter_by(customer=current_user, status='cart')
    
    return render_template('shopping_cart.html', cart_items=cart_items, title='Your cart')
    
@bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if current_user.is_anonymous:
        flash('Please log in!')
        return jsonify({'message': 'You have to sign in to add a product to the cart!'}), 401

    data = request.get_json()
    product_id = data.get('product_id')

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found!'}), 404
    
    OrderItem.add_to_cart(product, current_user)

    cart_count = OrderItem.query.filter_by(customer=current_user, status='cart').count()
    
    return jsonify({'message': 'Product added to the cart', 'cart_count': cart_count})

@bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if current_user.is_anonymous:
        return jsonify({'message': 'You are not permitted for this action!'}), 401
    
    data = request.get_json()
    product_id = data.get('product_id')

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found!'}), 404
    
    in_cart = OrderItem.query.filter_by(product=product, customer=current_user, status='cart').first()
    if in_cart.quantity >= 1:
        db.session.delete(in_cart)    
        db.session.commit()

    cart_items = OrderItem.query.filter_by(customer=current_user, status='cart').all()
    item_counts = {str(item.product_id): item.quantity for item in cart_items}
    cart_count = OrderItem.query.filter_by(customer=current_user, status='cart').count()
    
    return jsonify({'message': 'Product removed from the cart', 'item_counts': item_counts, 'cart_count': cart_count})

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
    
    in_cart = OrderItem.query.filter_by(product=product, customer=current_user, status='cart').first()
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
    cart_items = OrderItem.query.filter_by(customer=current_user, status='cart').all()
    item_counts = {str(item.product_id): item.quantity for item in cart_items}

    return jsonify({'item_counts': item_counts})

@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    form = CheckoutForm()
    customer_info = EditProfileForm(current_user.username)
    customer_info.username.data = current_user.username
    customer_info.delivery_address.data = current_user.delivery_address
    customer_info.phone_number.data = current_user.phone_number
    cart_items = OrderItem.query.filter_by(customer=current_user, status='cart').all()
    total_pay = sum(item.product.price * item.quantity for item in cart_items)
    
    
    if form.validate_on_submit():
        payment_type = form.payment_type.data
        order = Order(status = 'in_process',
                      items = cart_items,
                      customer = current_user,
                      total_pay = total_pay,
                      payment_type = payment_type
                      )
        for item in cart_items:
            db.session.add(item)
        db.session.add(order)
        db.session.commit()

        OrderItem.clear_cart(current_user)

        flash('Your order placed successfully!')
        order.send_order_confirmation()
        return redirect(url_for('main.load_customer', username=current_user.username))
    
    return render_template('checkout.html', title=('Checkout'), form=form, customer_info=customer_info, cart_items=cart_items, total_pay=total_pay)

@bp.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    pass

@bp.route('/search')
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    products, total = Product.search(g.search_form.q.data, page,
                               current_app.config['PROD_PER_PAGE'])
    next_url = None
    prev_url = None
    return render_template('search.html', title=('Search'), products=products,
                           next_url=next_url, prev_url=prev_url)