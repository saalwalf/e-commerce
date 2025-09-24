import os

# Konfigurasi
DB_USER = os.environ.get('DB_USER', 'avnadmin')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'AVNS_5uWfMJdXQckEpSGCNuB')
DB_HOST = os.environ.get('DB_HOST', 'mysql-235e404e-saalwalf-de4c.e.aivencloud.com')
DB_NAME = os.environ.get('DB_NAME', 'defaultdb')
DB_PORT = os.environ.get('DB_PORT', '19635')
CA_CERT_PATH = os.environ.get('CA_CERT_PATH', 'ca.pem')

SQLALCHEMY_DATABASE_URI = (
    f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)

SQLALCHEMY_TRACK_MODIFICATIONS = False
