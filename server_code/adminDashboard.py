import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import datetime

def get_admin_requests(month):
    users = app_tables.users.search(confirmed_email=True)
    
    if not month:
        return users
    
    # Get the start and end of the given month
    current_year = datetime.now().year
    start_date = datetime.datetime(current_year, month, 1)
    if month.month == 12:
        end_date = datetime.datetime(current_year + 1, 1, 1)
    else:
        end_date = datetime.datetime(current_year, month + 1, 1)

    # Filter users based on request time


  
    filtered_users = [
        user for user in users
        if any(req['timestamp'] >= start_date and req['timestamp'] < end_date
               for req in app_tables.requests.search(user=user))
    ]
    
    return filtered_users

  
