from . import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)  # auto-increment by default
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    image_url = db.Column(db.String(255))
    brand = db.Column(db.String(100))
    category = db.Column(db.String(100))  # running, walking, soccer, basketball, sneakers, sandals

    cart_items = db.relationship('CartItem', backref='product', lazy=True)    # relasi ke CartItem, satu product bisa ada di banyak cart (akses: product.cart_items/cart_item.product)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)  # relasi ke OrderItem, satu product bisa ada di banyak order (akses: product.order_items/order_item.product)
        
class ProductDetails(db.Model):
    __tablename__ = 'product_details'
    id = db.Column(db.Integer, primary_key=True)  # auto-increment by default
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    stock = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String(50))
    color = db.Column(db.String(50))
    
    product = db.relationship('Product',
                              backref=db.backref('details', lazy=True, cascade="all, delete-orphan")) # relasi ke Product
    
    def update_stock(self, new_stock):
        self.stock = new_stock
        db.session.commit()

    def update_price(self, new_price):
        self.price = new_price
        db.session.commit()