from flask import render_template
from app.main import bp
from app.models import Product



@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('products.html')


@bp.route('/products', methods=['GET', 'POST'])
def products():
    products = Product.query.all()

    return render_template('products.html', title=('Products'), products=products)


@bp.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    pass


@bp.route('/shopping_cart', methods=['GET', 'POST'])
def shopping_cart():
    pass


@bp.route('/search', methods=['POST'])
def search():
    pass