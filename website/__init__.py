from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from os import path
from werkzeug.security import generate_password_hash
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
from .row_test import get_date, get_credentials


db = SQLAlchemy()
migrate = Migrate()  
DB_NAME = "database.db"


def create_app(): # Create and configure the Flask application
    app = Flask(__name__)
    #start_scheduler()  # Start the scheduler to update the date daily
    app.config['SECRET_KEY'] = 'hjshjhdjah kjssaddshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    daily_date_update()  # Update the date in the spreadsheet daily
    
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


def initialize_admin(app): # Initialize admin user if not exists
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
    
def daily_date_update():
    spreadsheet = get_credentials()
    today = get_date()
    for worksheet in spreadsheet.worksheets():
        col_a = worksheet.col_values(1)
        if today not in col_a and len(col_a) > 2:            
            col_b = worksheet.col_values(2)
            row = len(col_b) + 2
            worksheet.update_cell(row, 1, today)
        elif today not in col_a and len(col_a) <= 2: # If there are no entries yet
            worksheet.update_cell(3, 1, today)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(daily_date_update, 'cron', day_of_week='mon-fri', hour=0, minute=1)
    scheduler.start()
   
