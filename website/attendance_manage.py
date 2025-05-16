from .row_test import get_credentials, get_time, get_date, targetrow, dateget, date_match
    
def handle_attendance(user, action):
    try:
        creds = get_credentials()
        worksheet = creds.worksheet(user.username)
        date = get_date()
        row = dateget()
        tdate = worksheet.cell(row, 1).value
        frow = date_match(worksheet, tdate, row)

        if tdate != date:
            worksheet.update_cell(frow, 1, date)

        Time = get_time()
        Cell = targetrow()

        if action == 'time_in':
            if worksheet.cell(Cell - 1, 3).value:
                return False, 'You haven\'t timed out yet!'
            worksheet.update_cell(Cell, 2, Time)
            worksheet.update_cell(Cell, 3, '')
            worksheet.update_cell(Cell + 1, 3, 'Total:')
            return True, 'Time in recorded!'

        elif action == 'time_out':
            if not worksheet.cell(Cell - 1, 2).value:
                return False, 'You haven\'t timed in yet!'

            if worksheet.cell(Cell - 1, 3).value and worksheet.cell(Cell - 1, 3).value != 'Total:':
                return False, 'You have already timed out!'

            # Insert your computation logic here...
            worksheet.update_cell(Cell - 1, 3, Time)
            worksheet.update_cell(Cell - 1, 4, f'=C{Cell-1}-B{Cell-1}')
            return True, 'Time out recorded!'

        return False, 'Invalid action'

    except Exception as e:
        return False, f'Error: {str(e)}'
