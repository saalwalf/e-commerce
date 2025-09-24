# app1.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, Flask
from models import db, Product, ProductDetails, User, Cart, CartItem, Order, OrderItem
import config

shop_bp = Blueprint(
    "shop",
    __name__,
    template_folder="../velora_bold_brands/templates",
    static_folder="../velora_bold_brands/static"
)

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

def get_products_with_details():
    """Get all products with their details for display"""
    products = []
    db_products = Product.query.all()
    
    for product in db_products:
        detail = ProductDetails.query.filter_by(product_id=product.id).first()
        product_data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'image_url': product.image_url,
            'brand': product.brand,
            'category': product.category,
            'type': product.product_type,
            'price': detail.price if detail else 0,
            'stock': detail.stock if detail else 0,
            'size': detail.size if detail else '',
            'color': detail.color if detail else ''
        }
        products.append(product_data)
    return products

def distinct(field):
    """Get distinct values for a field from products"""
    products = get_products_with_details()
    return sorted({p.get(field) for p in products if p.get(field)})

def find_product(pid: int):
    """Find a product by ID"""
    products = get_products_with_details()
    return next((p for p in products if p["id"] == pid), None)

def get_cart():
    """Get cart from session"""
    return session.setdefault("cart", {})

def cart_items():
    """Get cart items with product details"""
    c = get_cart()
    items = []
    for pid, qty in c.items():
        p = find_product(int(pid))
        if p:
            items.append({"product": p, "qty": qty})
    return items

@shop_bp.context_processor
def inject_nav():
    def safe_distinct(field):
        try:
            return distinct(field)
        except Exception:
            return []
    return {
        "NAV": [
            {"name": "Home", "endpoint": "shop.index"},
            {"name": "Produk", "endpoint": "shop.products_list"},
            {"name": "Keranjang", "endpoint": "shop.cart_page"},
            {"name": "Checkout", "endpoint": "shop.checkout"},
        ],
        "distinct": safe_distinct
    }

@shop_bp.route("/")
def index():
    products = get_products_with_details()
    return render_template("index.html", items=products[:8])

@shop_bp.route("/products")
def products_list():
    q = (request.args.get("q") or "").strip().lower()
    brand = request.args.get("brand") or ""
    category = request.args.get("category") or ""
    ptype = request.args.get("type") or ""

    items = get_products_with_details()
    if q:
        items = [p for p in items if q in p["name"].lower() or q in p.get("description","").lower()]
    if brand:
        items = [p for p in items if p.get("brand")==brand]
    if category:
        items = [p for p in items if p.get("category")==category]
    if ptype:
        items = [p for p in items if p.get("type")==ptype]

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 12))
    start = (page-1)*limit
    end = start+limit
    total = len(items)
    pages = (total + limit - 1)//limit
    view = items[start:end]

    return render_template("products/list.html",
        items=view, total=total, pages=pages, page=page, limit=limit,
        q=q, brand=brand, category=category, ptype=ptype,
        brands=distinct("brand"), categories=distinct("category"), types=distinct("type"))

@shop_bp.route("/products/<int:pid>")
def product_detail(pid):
    item = find_product(pid)
    if not item:
        flash("Produk tidak ditemukan", "danger")
        return redirect(url_for("shop.products_list"))
    return render_template("products/detail.html", item=item)

@shop_bp.route("/cart")
def cart_page():
    return render_template("cart.html", items=cart_items())

@shop_bp.post("/cart/add/<int:pid>", endpoint="cart_add")
def cart_add(pid):
    item = find_product(pid)
    if not item:
        return redirect(url_for("shop.products_list"))
    qty = max(1, int(request.form.get("qty", 1)))
    cart = get_cart()
    cart[str(pid)] = cart.get(str(pid), 0) + qty
    session.modified = True
    flash(f"{item['name']} ditambahkan ke keranjang.", "success")
    return redirect(request.referrer or url_for("shop.cart_page"))

@shop_bp.post("/cart/update")
def cart_update():
    new = {}
    for k,v in request.form.items():
        if k.startswith("qty_"):
            pid = k.split("_",1)[1]
            try: q = max(0, int(v))
            except: q = 0
            if q>0: new[pid]=q
    session["cart"] = new
    session.modified=True
    flash("Keranjang diperbarui.", "success")
    return redirect(url_for("shop.cart_page"))

@shop_bp.post("/cart/clear")
def cart_clear():
    session["cart"] = {}
    session.modified=True
    flash("Keranjang dikosongkan.", "info")
    return redirect(url_for("shop.cart_page"))

@shop_bp.route("/checkout", methods=["GET","POST"])
def checkout():
    items = cart_items()
    if request.method == "POST":
        if not items:
            flash("Keranjang kosong.", "danger")
            return redirect(url_for("shop.products_list"))
        
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip()
        address = (request.form.get("address") or "").strip()
        note = (request.form.get("note") or "").strip()
        
        if not name or not email or not address:
            flash("Lengkapi data checkout.", "danger")
            return render_template("checkout.html", items=items)
        
        orders = session.setdefault("orders", [])
        order = {
            "id": len(orders)+1,
            "name": name,
            "email": email,
            "address": address,
            "note": note,
            "items": items
        }
        orders.append(order)
        session["cart"] = {}
        session.modified = True
        flash("Order berhasil dibuat!", "success")
        return redirect(url_for("shop.order_success", oid=order["id"]))
    
    return render_template("checkout.html", items=items)

@shop_bp.route("/orders/<int:oid>")
def order_success(oid):
    orders = session.get("orders", [])
    order = next((o for o in orders if o["id"]==oid), None)
    if not order:
        flash("Order tidak ditemukan.", "danger")
        return redirect(url_for("shop.products_list"))
    return render_template("order_success.html", order=order)

@shop_bp.get("/api/products")
def api_products():
    products = get_products_with_details()
    return jsonify(products)

app.register_blueprint(shop_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
