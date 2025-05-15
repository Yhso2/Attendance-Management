from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .row_test import *
from . import db
import json
import gspread


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    creds = get_credentials()
    username = request.args.get('username')   
    worksheet= creds.worksheet(username)  # use username to get the specific sheet
    print("eto sheet name: ", username)
    
    date = get_date()
    row = dateget() 
    tdate= worksheet.cell(row,1).value      
    frow= date_match(tdate, row)
    
    if tdate != date:
     
     worksheet.update_cell(frow, 1, date)

    if request.method == 'POST': 
             Time = get_time()
             action = request.form['action']

             if action == 'time_in':
               Cell= targetrow()
               if worksheet.cell(Cell-1, 3).value is None or '':
                flash('You haven\'t timed out yet!', category='error')
               else:  
                 if worksheet.cell(Cell-1, 3).value != 'Total:':
                   worksheet.update_cell(Cell, 3, '')
                   worksheet.update_cell(Cell+1, 3, 'Total:')
                   
                 worksheet.update_cell(Cell, 2, Time)
                 flash('Time in recorded!', category='success')

             elif action == 'time_out':
             # Handle Time out action
              Cell= targetrow()
              if worksheet.cell(Cell-1, 2).value is None or '':
                  flash('You haven\'t timed in yet!', category='error')
              
              elif worksheet.cell(Cell-1, 3).value is not None and worksheet.cell(Cell-1, 3).value != 'Total:':
                  flash('You have already timed out!', category='error')
              else:
                total = Cell- 1 - row

                if total >= 1:
                   Upl = Cell - 1
                   Downl = Cell - (total+1)
                   worksheet.update_cell(Cell, 3, 'Total:') 
                   #worksheet.update_cell(Cell, 4, '=TEXT(SUM(D'+str(Upl)+':D'+ str(Downl)+'), "hh:mm ") & " HOURS"')
                   worksheet.update_cell(Cell, 4, '=SUM(D'+str(Upl)+':D'+ str(Downl)+')  & " HOURS"') 
                   
                else:
                   Upl = Cell - 1
                   worksheet.update_cell(Cell-1, 4, '=(C'+str(Upl)+'-B'+str(Upl)+') & " HOURS"') 

                worksheet.update_cell(Cell-1, 3, Time)
                difrow= Cell-1
                '=TRUNC((TIMEVALUE(C7) - TIMEVALUE(B7)) * 24) + ROUND(MOD((TIMEVALUE(C7) - TIMEVALUE(B7)) * 24, 1) * 60, 0) / 100'
                worksheet.update_cell(Cell-1, 4,  '=TRUNC((TIMEVALUE(C'+str(Upl)+') - TIMEVALUE(B'+str(Upl)+')) * 24) + ROUND(MOD((TIMEVALUE(C'+str(Upl)+') - TIMEVALUE(B'+str(Upl)+')) * 24, 1) * 60, 0) / 100' )
                #worksheet.update_cell(Cell-1, 4,  '=(C'+str(Upl)+'-B'+str(Upl)+')')
                #worksheet.update_cell(Cell-1, 4, '=C' + str(difrow) + '-C' +str(difrow))
                flash('Time out recorded!', category='success')

    return render_template("home.html", user=current_user, username=username)

@views.route('/admin', methods=['GET', 'POST'])
@login_required
def homead():    
        if request.method == 'POST': 
             Time = get_time()
             action = request.form['action']

             if action == 'time_in':
              Cell= targetrow()
              #worksheet.update_cell({Cell}, 2, {Time})
              flash('Time in recorded!', category='success')

             elif action == 'time_out':
             # Handle Time out action
              flash('Time out recorded!', category='success')
             
        return render_template("admin.html", user=current_user)




