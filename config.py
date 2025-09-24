import os

# Konfigurasi
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')

# Path ke sertifikat CA yang sudah Anda download dari Aiven
CA_CERT_PATH = os.environ.get('CA_CERT_PATH')

SQLALCHEMY_DATABASE_URI = (
    f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    f'?ssl_ca={CA_CERT_PATH}'
)

SQLALCHEMY_TRACK_MODIFICATIONS = False
