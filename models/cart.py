from . import db

class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)  # auto-increment by default
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade="all, delete-orphan") # relasi ke CartItem

    def add_item(self, product_id, quantity):
        item = CartItem.query.filter_by(cart_id=self.id, product_id=product_id).first()
        if item:
            item.quantity += quantity
        else:
            item = CartItem(cart_id=self.id, product_id=product_id, quantity=quantity)
            db.session.add(item)
        db.session.commit()

    def remove_item(self, product_id):
        item = CartItem.query.filter_by(cart_id=self.id, product_id=product_id).first()
        if item:
            db.session.delete(item)
            db.session.commit()

    def clear_cart(self):
        CartItem.query.filter_by(cart_id=self.id).delete()
        db.session.commit()

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)