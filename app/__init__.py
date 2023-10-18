from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap5 import Bootstrap
from flask_admin import Admin


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

    from app.admin_panel.routes import ProductsAdminView
    admin.add_view(ProductsAdminView(models.Products, db.session))

    return app

from app import models