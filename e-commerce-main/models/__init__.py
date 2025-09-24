from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .product import Product, ProductDetails
from .cart import Cart, CartItem
from .order import Order, OrderItem