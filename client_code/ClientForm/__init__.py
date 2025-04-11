from ._anvil_designer import ClientFormTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ClientForm(ClientFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.user = anvil.users.get_user()
    self.init_components(**properties)
    self.label_3.text = f"{self.user['admin_name']} Admin"
    self.repeating_panel_1.items = anvil.server.call('get_all_clients')
    self.repeating_panel_2.items = anvil.server.call('get_notifaicatons')
 
    # Any code you write here will run when the form opens.

  def button_5_click(self, **event_args):
    open_form('admin_dashboard')

  def button_3_click(self, **event_args):
    open_form('Settings')

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    alert("Users logged out successfully")
    open_form('Form1')
