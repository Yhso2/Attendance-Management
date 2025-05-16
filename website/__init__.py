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
    
    initialize_admin(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return emp.query.get(int(id))

    return app


def initialize_admin(app):
    with app.app_context():
        from .models import emp   
        db_path = path.join(app.instance_path, DB_NAME)    
        if not path.exists(db_path):
             print("[INFO] No DB found. Please run 'flask db upgrade' to create schema.")
             return 
                
        if not emp.query.filter_by(username='admin').first():
            admin_user = emp(username='admin', 
                             fname='admin', 
                             name='admin', 
                             password=generate_password_hash('admin'))
            try:
                db.session.add(admin_user)
                db.session.commit()
                print("[INFO] Admin user created successfully.")
            except Exception as e:
                db.session.rollback()
                print(f"[ERROR] Failed to create admin user: {e}")
            

   
