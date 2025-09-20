from . import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)  # auto-increment by default
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending') # pending, paid, shipped, completed, cancelled
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    total_price = db.Column(db.Float, default=0.0)

    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")

    def update_status(self, new_status):
        self.status = new_status
        db.session.commit()

    def update_address(self, new_address):
        self.address = new_address
        db.session.commit()

    def update_phone(self, new_phone):
        self.phone = new_phone
        db.session.commit()

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)