from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from os import path
from werkzeug.security import generate_password_hash
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()  
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjssaddshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app)   
    migrate.init_app(app, db) 

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')        
   
   
    from .models import emp
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return emp.query.get(int(id))

    return app


def create_database(app):
    from .models import emp
    from . import db
    if not path.exists('instance/' + DB_NAME):     
        with app.app_context():
            db.create_all()  
            admin_user = emp(username='admin', fname='admin', name='admin', password=generate_password_hash('admin'))
            try:
                db.session.add(admin_user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                
   
        
