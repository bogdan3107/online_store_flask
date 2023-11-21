from app import db, login, mail
from datetime import datetime, time
from flask import current_app, render_template, json
from flask_login import UserMixin, current_user
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from app.search import add_to_index, remove_from_index, query_index
import jwt

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(*when, value=cls.id)), total


    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

product_category_association = db.Table(
    'product_category_association',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', back_populates='order_items', lazy=True)
    quantity = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    status = db.Column(db.String(16), default='cart', server_default='cart')
    order = db.relationship('Order', back_populates='items')
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer = db.relationship('User', back_populates='order_item')
    
    @classmethod
    def add_to_cart(cls, product, customer):
        in_cart = OrderItem.query.filter_by(product=product, customer=customer, status='cart').first()
        if in_cart:
            in_cart.quantity += 1
        else:
            cart = OrderItem(product=product, quantity=1, customer=current_user)
            db.session.add(cart)

        db.session.commit()

        return in_cart
    
    @classmethod
    def clear_cart(cls, customer):
        cart_items = cls.query.filter_by(customer=customer, status='cart').all()
        for cart_item in cart_items:
            db.session.delete(cart_item)
        db.session.commit()
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    status = db.Column(db.String(16), default='cart', server_default='cart')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    customer = db.relationship('User', back_populates='orders')
    total_pay = db.Column(db.Float)
    payment_type = db.Column(db.String(32))
    payment_status = db.Column(db.Boolean, default=False)

    def send_order_confirmation(self):
        try:
            customer = self.customer
            order_items = []
            for item in self.items:
                order_items.append({'name': item.product.name,
                                    'quantity': item.quantity,
                                    'price': item.product.price * item.quantity})
                
            msg = Message('[Glo Shop] Order {} confirmed'.format(self.id),
                          sender=current_app.config['ADMINS'][0],
                          recipients=[customer.email])
            msg.body = render_template('email/order_confirmation.txt', user=customer)
            msg.html = render_template('email/order_confirmation.html', user=customer)

            msg.attach('order.json', 'application/json', json.dumps({'order': order_items}, indent=4))

            mail.send(msg)
        except Exception as e:
            print(f"error sending order confirmation email: {e}")

   
class Product(SearchableMixin, db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    description = db.Column(db.String(140))
    image_path = db.Column(db.String(255))
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', secondary=product_category_association, back_populates='products')
    order_items = db.relationship('OrderItem', back_populates='product', lazy=True)

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, stock={self.stock}, order_items={getattr(self, 'order_items', None)})>"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    products = db.relationship('Product', secondary=product_category_association, back_populates='category')

    def __repr__(self) -> str:
        return f"Category(id={self.id}, name={self.name})"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    phone_number = db.Column(db.String(32))
    delivery_address = db.Column(db.String(128))
    orders = db.relationship('Order', back_populates='customer')
    order_item = db.relationship('OrderItem', back_populates='customer')
    
    def __repr__(self) -> str:
        return '<User {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
