from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .row_test import *
from . import db
from .attendance_manage import handle_attendance




views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():    
    username = request.args.get('username') 
    message = ''     
  # date_update(current_user)  # Ensure the date is updated for the current user
    if request.method == 'POST':              
             action = request.form['action']
             success, message = handle_attendance(current_user, action)
             
    return render_template("home.html", user=current_user, username=username, message=message)

@views.route('/admin', methods=['GET', 'POST'])
@login_required
def homead():    
        if request.method == 'POST': 
             Time = get_time()
             action = request.form['action']

             if action == 'time_in':
              Cell= target_row()
              #worksheet.update_cell({Cell}, 2, {Time})
              flash('Time in recorded!', category='success')

             elif action == 'time_out':
             # Handle Time out action
              flash('Time out recorded!', category='success')
             
        return render_template("admin.html", user=current_user)




