from ._anvil_designer import signUpReqquestStatusTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server


class signUpReqquestStatus(signUpReqquestStatusTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

  def get_status(self):
    if self.item['status']:
      return 'Accepted'
    elif self.item['status'] == False:
      return 'Rejected'
    else:
      return 'Pending'

  def get_background_color(self):
    if self.item['status']:
      return 'green'
    elif self.item['status'] == False:
      return 'red'
    else:
      return 'orange'

  def button_1_click(self, **event_args):
    open_form('PaymentForm')

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    response = alert("Are you sure you want to Logout?", buttons=["Yes", "No"])
    if response == "Yes":
      anvil.server.session["authenticated"] = False
      anvil.users.logout()
      alert("Users logged out successfully")
      open_form('Form1')

  def policy_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ServicePage')

  def privacy_statement_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('PrivacyPolicy')
