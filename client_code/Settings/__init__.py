from ._anvil_designer import SettingsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Settings(SettingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.user = anvil.users.get_user()
    
    self.init_components(**properties)
    self.text_box_1.text = self.user['email']
    self.label_3.text = f"{self.user['admin_name']} Admin"
    # self.user['email']

    # Any code you write here will run when the form opens.

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    response = alert("Are you sure you want to Logout?", buttons=["Yes", "No"])
    if response == "Yes":
      anvil.server.session["authenticated"] = False
      anvil.users.logout()
      alert("Users logged out successfully")
      open_form('Form1')
      
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('_send_password_reset', self.user['email'], True)
    alert(f"Reset password Email has been sent to {self.user['email']}")

  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin_dashboard')

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ClientForm')
