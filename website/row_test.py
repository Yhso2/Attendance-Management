import gspread
import datetime
import os
from oauth2client.service_account import ServiceAccountCredentials
# from google.oauth2 import service_account

def get_credentials():
    # Define the scope of Google Sheets API access
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    creds_path = os.path.join(BASE_DIR, 'creds.json')

    # Path to your service account JSON key file
    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)

    # Authenticate using the credentials
    gc = gspread.authorize(credentials)

    # Open the spreadsheet by its title
    spreadsheet = gc.open('DITO')
        
    return spreadsheet

# Helper function to get the worksheet by username if needed
def get_worksheet(username):
    spreadsheet = get_credentials()
    return spreadsheet.worksheet(username) 
   
def get_date():  # Get the current date and time
    return datetime.date.today().strftime("%m/%d/%y")

def get_time():  # Returns formatted time as 12hr am/pm (e.g., 2:30 PM)
    return datetime.datetime.now().strftime("%I:%M %p")

def get_row(worksheet, column): # Get the last non-empty row in column 
    column_values = worksheet.col_values(column)  # Get all values from the specified column    
    for i in reversed(range(len(column_values))): # Iterate through the column values in reverse order
        if column_values[i].strip() and column_values[i] not in ("Date", "Time-In"):  # Check if the cell value is not empty
           return i + 1
        else:
            return 3 # Return 3 if no date is found in the column

def check(worksheet, cell, column):    
    if worksheet.cell(cell, column).value is None or '':
      return True
    else:
      return False
                          
def target_row(worksheet, row):     
    column_values = worksheet.col_values(2)
    col_len = len(column_values)
    if col_len < row:
        return row
    elif col_len >= row:
        return row + (col_len - row) + 1


def date_update(user): # To be run in views :: Checks if the current date is already in the worksheet, if not, it adds it
    worksheet = get_credentials().worksheet(user.username)    
    current_date = get_date()
    latest_date = worksheet.cell(get_row(worksheet, 1), 1).value   # Get the latest date in column A
    if latest_date != current_date:
        worksheet.update_cell(get_row(worksheet, 2) + 2, 1, current_date)

