from ._anvil_designer import admin_dashboardTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class admin_dashboard(admin_dashboardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.user = anvil.users.get_user()
    self.clients_count = anvil.server.call('get_all_clients_count')
    self.init_components(**properties)
    self.label_3.text = f"{self.user['admin_name']} Admin"
    self.repeating_panel_3.items = anvil.server.call('get_admin_requests')
    self.all_clients = anvil.server.call('get_all_clients')
    self.repeating_panel_1.items = self.all_clients
    self.repeating_panel_2.items = anvil.server.call('get_notifaicatons')
    self.drop_down_1.items = ['','January',
                              'February',
                              'March',
                              'April',
                              'May',
                              'June',
                              'July',
                              'August',
                              'September', 
                              'October', 
                              'November',
                              'December']
    

    # Any code you write here will run when the form opens.

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    
    self.repeating_panel_3.items = anvil.server.call('get_admin_requests', self.drop_down_1.selected_value)
    self.refresh_data_bindings()

    # self.clients_count = anvil.server.call('get_all_clients_count')

  def get_clients_count(self):
    return self.clients_count

  def get_admins_count(self):
    return self.clients_count

  def button_1_click(self, **event_args):
    open_form('ClientForm')

  def button_4_click(self, **event_args):
    open_form('ClientForm')

  def button_3_click(self, **event_args):
    open_form('Settings')

  def button_2_click(self, **event_args):
    anvil.users.logout()
    open_form('Form1')
    