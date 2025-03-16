import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def get_user_cleint(user):
  return app_tables.clients.get(user=user)

@anvil.server.callable
def get_notifaicatons():
  return app_tables.notifications.search(tables.order_by('created_at'))