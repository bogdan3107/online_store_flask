from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap5 import Bootstrap
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
admin = Admin(name='Store admin', template_mode='bootstrap3')




def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    admin.init_app(app)

    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.admin_panel import bp as admin_panel_bp
    admin_panel_bp.name = 'my_admin_panel_bp'
    app.register_blueprint(admin_panel_bp)

    from app import models

    from app.admin_panel.routes import ProductsAdminView, CategoryAdminView
    file_admin = FileAdmin(app.config['PRODUCT_IMAGE_DIR'], 
                       name='Images', endpoint='images', url='/admin/images')
    admin.add_view(ProductsAdminView(models.Product, db.session))
    admin.add_view(CategoryAdminView(models.Category, db.session))
    admin.add_view(file_admin)

    return app

from app import models