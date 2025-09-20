import os

# Konfigurasi
DB_USER = os.environ.get('DB_USER', 'sql12799361')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'TfjIrGfGyi')
DB_HOST = os.environ.get('DB_HOST', 'sql12.freesqldatabase.com')
DB_NAME = os.environ.get('DB_NAME', 'sql12799361')

SQLALCHEMY_DATABASE_URI = (
    f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}'
)

SQLALCHEMY_TRACK_MODIFICATIONS = False