from flask import render_template, current_app, json, redirect, url_for, flash, request
from app.main import bp
from app.models import Product
import json



@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('products.html')


@bp.route('/products', methods=['GET', 'POST'])
def products():
    products = Product.query.all()

    return render_template('products.html', title=('Products'), products=products)


@bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    pass


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