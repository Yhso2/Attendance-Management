from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import emp
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from .row_test import *
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account


auth = Blueprint('auth', __name__)

# Define the scope of Google Sheets API access
#scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Path to your service account JSON key file
#credentials = ServiceAccountCredentials.from_json_keyfile_name('bcreds.json', scope)

# Authenticate using the credentials
#gc = gspread.authorize(credentials)

# Open the spreadsheet by its title
#spreadsheet = gc.open('DITO')

# Select a specific worksheet within the spreadsheet by its title
#worksheet = spreadsheet.worksheet('Sheet1')  # Change 'Sheet1' to your worksheet name

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': 
        
        username = request.form.get('username') 
        password = request.form.get('password')
        user = emp.query.filter_by(username=username).first()        
        if user.id == 1:          
          if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.homead'))
          else:
                flash('Incorrect password, try again.', category='error')
                
        
        elif user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home', username=user.fname, usersheet=user.fname))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))




@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        spreadsheet = get_credentials()
        
        username = request.form.get('username')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = emp.query.filter_by(username=username).first()
        if user: #any(username in user_data)
            flash('Username already exists.', category='error')
        elif len(username) < 4:
            flash('Username must be greater than 3 characters.', category='error')
        elif len(first_name) < 1:
            flash('First name must NOT be empty.', category='error')
        elif len(last_name) < 1:
            flash('Last name must NOT be empty.', category='error')    
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 5:
            flash('Password must be at least 7 characters.', category='error')
        else:
            #spreadsheet = gc.create(first_name)
            worksheet = spreadsheet.add_worksheet(title=first_name, rows=100, cols=20)
            values = [
             ['Name :', first_name, '', ''],  # Row 1
             ['Date', 'Time-In', 'Time-out','Number of hours'],]  # Row 2
            worksheet.update('A1:D2', values)
            new_user = emp(username=username, fname= first_name, name=first_name+' '+last_name, password=generate_password_hash(password1))
            #add_user_to_google_spreadsheet(username, first_name, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home', username=first_name, usersheet=first_name))

    return render_template("sign_up.html", user=current_user)








@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')

        if not check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect.', category='error')
        elif new_password != confirm_new_password:
            flash('New passwords do not match.', category='error')
        elif len(new_password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            current_user.password = generate_password_hash(new_password)
            db.session.commit()
            flash('Password changed successfully!', category='success')
            return redirect(url_for('views.home'))  # Update the redirect URL as needed

    return render_template("changepass.html", user=current_user)

