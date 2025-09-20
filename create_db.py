from app import app
from models import db

with app.app_context():
    db.drop_all()      # delete
    db.create_all()    # recreate
    print("Database tables dropped and recreated!")
    
# Check apakah tabel sudah terbuat
with app.app_context():
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print("Existing tables in the database:", tables)