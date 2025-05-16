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

    # Select a specific worksheet within the spreadsheet by its title
    #worksheet = spreadsheet.worksheet('Sheet1')  # Change 'Sheet1' to your worksheet name
        
    return spreadsheet


def get_worksheet(username):
    spreadsheet = get_credentials()
    return spreadsheet.worksheet(username) 
   


def get_date():
    # Get the current date and time
    current_datetime = datetime.date.today()    
    # Format date as m/d/y (e.g., 4/18/2024)
    formatted_date = current_datetime.strftime("%m/%d/%y") 
    return formatted_date


def get_time():
    # Get the current date and time
    current_datetime = datetime.datetime.now()
     # Format time as 12hr am/pm (e.g., 2:30 PM)
    formatted_time = current_datetime.strftime("%I:%M %p")
    return formatted_time


def date_match(worksheet, rowval, trow):
    rownum = trow
    crnt_date = get_date()
    Colb_values = worksheet.col_values(2)
    if rowval == crnt_date: # Same date following time-in
       if len(Colb_values)<rownum:
          return rownum
       else:    
        if len(Colb_values) > rownum:
         diff = len(Colb_values) - rownum
         rownum = rownum+1+diff
         return rownum
        else:
           return rownum+1
    else: # Not the same date
        rownum+=1 
        
    if len(Colb_values) < rownum : # checks len of column B
     return rownum  # Exit the loop  
    else:
     diff = len(Colb_values) - rownum
     return rownum+diff+2 # Exit the loop     #Plus 1 kase space for sa total hours of the day
    

def dateget(worksheet):
    # Get all values from the specified column
    column_values = worksheet.col_values(1)    
    # Iterate through the column values in reverse order
    for i in range(len(column_values) - 1, -1, -1):
        if column_values[i]:  
           return i + 1

def check(worksheet, cell, column):    
    if worksheet.cell(cell, column).value is None or '':
      return True
    else:
      return False
                          


def targetrow(worksheet):    
    trow = None
    rowval = None   
    # Get all values from the specified column
    column_values = worksheet.col_values(1)    
    # Iterate through the column values in reverse order
    for i in range(len(column_values) - 1, -1, -1):
        if column_values[i]:  # Check if the cell value is not empty
         trow = i + 1  # Convert zero-based index to 1-based row number
         rowval = column_values[i] 
         break  # Stop once the last non-empty cell is found  

    if trow is not None and trow != 2:   
     # Store the value of the last non-empty cell as a variable
     target = date_match(worksheet, rowval, trow) 
     return target    
    else: 
     return trow+1
