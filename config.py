import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, 'env'))

image_dir = 'app/static/dump'


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRODUCT_IMAGE_DIR = os.path.join(basedir, image_dir)
    TEMP_CART_KEY = 'TEMP_CART'
    MAIL_SERVER = '127.0.0.1'
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['admin@gloshop.com']
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    PROD_PER_PAGE = 10