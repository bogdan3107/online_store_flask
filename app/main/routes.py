from flask import render_template
from app.main import bp



@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    products = [
            {   'name': 'Product1',
                'description': 'Here is decription of the first product',
                'image': 'dump/img1.jpg'
            },
            {   'name': 'Product2',
                'description': 'Here is decription of the second product',
                'image': 'dump/img2.jpg'
            },
            {   'name': 'Product2',
                'description': 'Here is decription of the second product',
                'image': 'dump/img2.jpg'
            },
            {   'name': 'Product2',
                'description': 'Here is decription of the second product',
                'image': 'dump/img2.jpg'
            }
    ]
    return render_template('index.html', title=('Home'), products=products)