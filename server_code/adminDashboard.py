import anvil.files
from anvil.files import data_files
import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

@anvil.server.callable
def get_admin_requests(month=None):
    users = app_tables.users.search(confirmed_email=True, is_admin=q.not_(True))
    clients = app_tables.clients.search(tables.order_by('requested_at', ascending=False),user=q.any_of(*users))
    
    if not month:
        return clients
    
    month_number = datetime.strptime(month, '%B').month
    current_year = datetime.now().year
    start_date = datetime(current_year, month_number, 1)
    if month_number == 12:
        end_date = datetime(current_year + 1, 1, 1)
    else:
        end_date = datetime(current_year, month_number + 1, 1)

    # Filter users based on request time
    users = app_tables.users.search(confirmed_email=True)
    clients = app_tables.clients.search(tables.order_by('requested_at', ascending=False),user=q.any_of(*users),requested_at=q.between(start_date, end_date))
    return clients
  
@anvil.server.callable
def get_all_clients():
  return app_tables.clients.search(tables.order_by('requested_at', ascending=False), status=True)

@anvil.server.callable
def get_admin_dashboard_data():
  users = app_tables.users.search(confirmed_email=True, is_admin=q.not_(True))
  clients_count = len(app_tables.clients.search(user=q.any_of(*users)))

  reviews_count = len(app_tables.reviews.search())

  admins_count = len(app_tables.users.search(is_admin=True))

  total_requests = len(app_tables.clients.search())

  accepted_requests = len(app_tables.clients.search(status=True))
  
  rejected_requests = len(app_tables.clients.search(status=False))
  
  return clients_count, reviews_count, admins_count, total_requests, accepted_requests, rejected_requests
  
