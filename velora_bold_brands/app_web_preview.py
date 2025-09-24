
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "dev")

from data.mock_products import PRODUCTS

def distinct(field):
    return sorted({p.get(field) for p in PRODUCTS if p.get(field)})

def find_product(pid:int):
    return next((p for p in PRODUCTS if p["id"]==pid), None)

def get_cart():
    return session.setdefault("cart", {})

def cart_items():
    c = get_cart()
    items = []
    for pid, qty in c.items():
        p = find_product(int(pid))
        if p:
            items.append({"product": p, "qty": qty})
    return items

@app.context_processor
def inject_nav():
    return {"NAV": [
        {"name":"Home", "endpoint":"index"},
        {"name":"Produk", "endpoint":"products_list"},
        {"name":"Keranjang", "endpoint":"cart_page"},
        {"name":"Checkout", "endpoint":"checkout"},
    ], "distinct": distinct}

@app.route("/")
def index():
    return render_template("index.html", items=PRODUCTS[:8])

@app.route("/products")
def products_list():
    q = (request.args.get("q") or "").strip().lower()
    brand = request.args.get("brand") or ""
    category = request.args.get("category") or ""
    ptype = request.args.get("type") or ""

    items = PRODUCTS
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
    start = (page-1)*limit; end = start+limit
    total = len(items); pages = (total + limit - 1)//limit
    view = items[start:end]

    return render_template("products/list.html",
        items=view, total=total, pages=pages, page=page, limit=limit,
        q=q, brand=brand, category=category, ptype=ptype,
        brands=distinct("brand"), categories=distinct("category"), types=distinct("type"))

@app.route("/products/<int:pid>")
def product_detail(pid):
    item = find_product(pid)
    if not item:
        flash("Produk tidak ditemukan", "danger")
        return redirect(url_for("products_list"))
    return render_template("products/detail.html", item=item)

@app.route("/cart")
def cart_page():
    return render_template("cart.html", items=cart_items())

@app.post("/cart/add/<int:pid>")
def cart_add(pid):
    item = find_product(pid)
    if not item: return redirect(url_for("products_list"))
    qty = max(1, int(request.form.get("qty", 1)))
    cart = get_cart()
    cart[str(pid)] = cart.get(str(pid), 0) + qty
    session.modified = True
    flash(f"{item['name']} ditambahkan ke keranjang.", "success")
    return redirect(request.referrer or url_for("cart_page"))

@app.post("/cart/update")
def cart_update():
    new = {}
    for k,v in request.form.items():
        if k.startswith("qty_"):
            pid = k.split("_",1)[1]
            try: q = max(0, int(v))
            except: q = 0
            if q>0: new[pid]=q
    session["cart"] = new; session.modified=True
    flash("Keranjang diperbarui.", "success")
    return redirect(url_for("cart_page"))

@app.post("/cart/clear")
def cart_clear():
    session["cart"] = {}; session.modified=True
    flash("Keranjang dikosongkan.", "info")
    return redirect(url_for("cart_page"))

@app.route("/checkout", methods=["GET","POST"])
def checkout():
    items = cart_items()
    if request.method == "POST":
        if not items:
            flash("Keranjang kosong.", "danger")
            return redirect(url_for("products_list"))
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip()
        address = (request.form.get("address") or "").strip()
        note = (request.form.get("note") or "").strip()
        if not name or not email or not address:
            flash("Lengkapi data checkout.", "danger")
            return render_template("checkout.html", items=items)
        orders = session.setdefault("orders", [])
        order = {"id": len(orders)+1, "name": name, "email": email, "address": address, "note": note, "items": items}
        orders.append(order); session["cart"] = {}; session.modified=True
        flash("Order berhasil dibuat. 🎉", "success")
        return redirect(url_for("order_success", oid=order["id"]))
    return render_template("checkout.html", items=items)

@app.route("/orders/<int:oid>")
def order_success(oid):
    orders = session.get("orders", [])
    order = next((o for o in orders if o["id"]==oid), None)
    if not order:
        flash("Order tidak ditemukan.", "danger")
        return redirect(url_for("products_list"))
    return render_template("order_success.html", order=order)

@app.get("/api/products")
def api_products():
    return jsonify(PRODUCTS)

if __name__ == "__main__":
    app.run(debug=True)
