from .row_test import get_credentials, get_time, target_row, get_row
from flask import flash
    
def handle_attendance(user, action):
    try:
        creds = get_credentials()
        worksheet = creds.worksheet(user.username)        

        Time = get_time()
        latest_date = get_row(worksheet, 1)
        Cell = target_row(worksheet, latest_date)
        entry_count = Cell - 1 - latest_date

        if action == 'time_in':
            if worksheet.cell(Cell-1, 3).value is None or '':
                flash('You haven\'t timed out yet!', category='error')
                return False, 'You haven\'t timed out yet!'
            else:
                if entry_count >= 1:
                    worksheet.update_cell(Cell + 1, 3, 'Total:')
                    worksheet.update_cell(Cell, 4, '')
                    worksheet.update_cell(Cell, 3, '')
                                    
                
            
            worksheet.update_cell(Cell, 2, Time)
            flash('Time in recorded!', category='success')
            return True, 'Time in recorded!'

        elif action == 'time_out':

            if not worksheet.cell(Cell - 1, 2).value: # Just to catcht if the user has not timed in :: Since it would see a blank if it a first entry on that day
                flash('You haven\'t timed in yet!', category='error')
                return False, 'You haven\'t timed in yet!'

            if worksheet.cell(Cell - 1, 3).value: # Since blank space have been checked, and poiter always moves one row down, this would check if time out has already been recorded
                flash('You have already timed out!', category='error')
                return False, 'You have already timed out!'
            else:
                if entry_count >= 1:
                    upper_limit = Cell - 1
                    lower_limit = Cell - (entry_count + 1)
                    worksheet.update_cell(Cell, 3, 'Total:') 
                    worksheet.update_cell(Cell, 4, '=SUM(D'+str(upper_limit)+':D'+ str(lower_limit)+')  & " Hours"')
                else:
                   upper_limit = Cell - 1
                   worksheet.update_cell(Cell-1, 4, '=(C'+str(upper_limit)+'-B'+str(upper_limit)+') & " HOURS"')

                worksheet.update_cell(Cell - 1, 3, Time)
                # Unsure which of this two lines is correct, but both are used to calculate the time difference
                worksheet.update_cell(Cell-1, 4,  '=TRUNC((TIMEVALUE(C'+str(upper_limit)+') - TIMEVALUE(B'+str(upper_limit)+')) * 24) + ROUND(MOD((TIMEVALUE(C'+str(upper_limit)+') - TIMEVALUE(B'+str(upper_limit)+')) * 24, 1) * 60, 0) / 100' )
                #worksheet.update_cell(Cell - 1, 4, f'=C{Cell-1}-B{Cell-1}')
                
                flash('Time out recorded!', category='success')
                return True, 'Time out recorded!'

        return False, 'Invalid action'

    except Exception as e:
        return False, f'Error: {str(e)}'
