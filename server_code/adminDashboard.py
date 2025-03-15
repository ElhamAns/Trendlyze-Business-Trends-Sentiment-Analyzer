import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import datetime

@anvil.server.callable
def get_admin_requests(month=None):
    users = app_tables.users.search(confirmed_email=True)
    clients = app_tables.clients.search(user=q.any_of(*users))
    
    if not month:
        return clients
    
    # Get the start and end of the given month
    current_year = datetime.now().year
    start_date = datetime.datetime(current_year, month, 1)
    if month.month == 12:
        end_date = datetime.datetime(current_year + 1, 1, 1)
    else:
        end_date = datetime.datetime(current_year, month + 1, 1)

    # Filter users based on request time
    users = app_tables.users.search(requested_at=q.between(start_date, end_date))
    return users

  
