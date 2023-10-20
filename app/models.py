from app import db
from datetime import datetime


product_category_association = db.Table(
    'product_category_association',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', back_populates='orders', lazy=True)
    quantity = db.Column(db.Integer)
    customer_name = db.Column(db.String(128), nullable=False)
    customer_phone = db.Column(db.String(32), nullable=False)
    customer_address = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(16), default='cart', server_default='cart') #'cart' or 'order'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Order(id={self.id}, product={self.product}, quantity={self.quantity}, status={self.status})"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    description = db.Column(db.String(140))
    image_path = db.Column(db.String(255))
    price = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', secondary=product_category_association, back_populates='products')
    orders = db.relationship('Order', back_populates='product', lazy=True)

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, stock={self.stock}, orders={getattr(self, 'orders', None)})>"
    


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    products = db.relationship('Product', secondary=product_category_association, back_populates='category')

    def __repr__(self) -> str:
        return f"Category(id={self.id}, name={self.name})"
    
    def add_category(name):
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return new_category


