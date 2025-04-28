from ._anvil_designer import clients_pageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class clients_page(clients_pageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.user = anvil.users.get_user()
    self.init_components(**properties)
    self.label_3.text = f"{self.user['admin_name']} Admin"

    # Any code you write here will run when the form opens.

  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    response = alert("Are you sure you want to Logout?", buttons=["Yes", "No"])
    if response == "Yes":
      anvil.server.call('get_session_unauthenticated')
      anvil.users.logout()
      alert("Users logged out successfully")
      open_form('Form1')
