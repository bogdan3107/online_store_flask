import logging
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap5 import Bootstrap
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf import CSRFProtect
from logging.handlers import SMTPHandler


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
admin = Admin(name='Store admin', template_mode='bootstrap3')
login = LoginManager()
mail = Mail()
#csrf = CSRFProtect()
logging.basicConfig(level=logging.DEBUG)




def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    admin.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    #csrf.init_app(app)

    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.admin_panel import bp as admin_panel_bp
    admin_panel_bp.name = 'my_admin_panel_bp'
    app.register_blueprint(admin_panel_bp)

    from app import models

    from app.admin_panel.routes import ProductsAdminView, CategoryAdminView, UserAdminView, OrderItemAdminView
    file_admin = FileAdmin(app.config['PRODUCT_IMAGE_DIR'], 
                       name='Images', endpoint='images', url='/admin/images')
    admin.add_view(ProductsAdminView(models.Product, db.session))
    admin.add_view(CategoryAdminView(models.Category, db.session))
    admin.add_view(UserAdminView(models.User, db.session))
    admin.add_view(OrderItemAdminView(models.OrderItem, db.session))
    admin.add_view(file_admin)


    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    return app

from app import models