from flask import render_template
from app.main import bp



@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@bp.route('/products', methods=['GET', 'POST'])
def products():
    products = [
            {   'name': 'Product1',
                'description': 'Here is decription of the first product',
                'image_path': 'dump/img1.jpg'
            },
            {   'name': 'Product2',
                'description': 'Here is decription of the second product',
                'image_path': 'dump/img2.jpg'
            },
            {   'name': 'Product2',
                'description': 'Here is decription of the second product',
                'image_path': 'dump/img2.jpg'
            },
            {   'name': 'Product2',
                'description': 'Here is decription of the second product',
                'image_path': 'dump/img2.jpg'
            }
    ]
    return render_template('index.html', title=('Products'), products=products)


@bp.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    pass


@bp.route('/shopping_cart', methods=['GET', 'POST'])
def shopping_cart():
    pass


@bp.route('/search', methods=['POST'])
def search():
    pass