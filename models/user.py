from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # auto-increment by default
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    cart = db.relationship('Cart', backref='user', uselist=False) # tiap user punya satu cart (akses: user.cart/cart.user)
    orders = db.relationship('Order', backref='user', lazy=True)  # tiap user bisa punya banyak order (akses: user.orders/order.user)

    def update_username(self, new_username):
        self.username = new_username
        db.session.commit()

    def update_email(self, new_email):
        self.email = new_email
        db.session.commit()

    def update_phone(self, new_phone):
        self.phone = new_phone
        db.session.commit()