import pandas as pd
from app import app
from models import db, Product, ProductDetails

with app.app_context():
    db.drop_all()      # delete
    db.create_all()    # recreate
    print("Database tables dropped and recreated!")
    
# Check apakah tabel sudah terbuat
with app.app_context():
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print("Existing tables in the database:", tables)
    
# Menambahkan produk awal
# Load excel
excel_file = 'initial_product.xlsx'
products_df = pd.read_excel(excel_file, sheet_name='products')
details_df = pd.read_excel(excel_file, sheet_name='product_details')

with app.app_context():
    # Insert Products
    for _, row in products_df.iterrows():
        product = Product(
            id = row['id'],
            name=row['name'],
            description=row['description'],
            image_url=row['image_url'],
            brand=row['brand'],
            category=row['category'],
            product_type=row['type']
        )
        db.session.add(product)
    db.session.commit()

    # Insert ProductDetails
    for _, row in details_df.iterrows():
        detail = ProductDetails(
            id=row['id'],
            product_id=row['product_id'],  # ForeignKey to Product.id
            stock=row['stock'],
            price=row['price'],
            size=row['size'],
            color=row['color']
        )
        db.session.add(detail)
    db.session.commit()
    
# Cek isi database
with app.app_context():
    products = Product.query.all()
    details = ProductDetails.query.all()
    
    print("\nProducts in database:")
    for product in products:
        print(f"ID: {product.id}, Name: {product.name}, Brand: {product.brand}, Category: {product.category}, Type: {product.product_type}")
    
    print("\nProduct Details in database:")
    for detail in details:
        print(f"ID: {detail.id}, Product ID: {detail.product_id}, Stock: {detail.stock}, Price: {detail.price}")