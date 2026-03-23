import os

class Config:
    # Ruta de la base de datos
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'university.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'password123' 
    ODOO_URL = 'http://localhost:8069'
    ODOO_DB = 'university_new'
    ODOO_USER = 'luciomalgiogliopl3@gmail.com'
    ODOO_PASS = 'password'