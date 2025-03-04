from ._anvil_designer import registerTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server


class register(registerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('login')
    pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.email != self.confirm_email:
      alert("Email and Confirm email must be same")
      return
    if len(self.passwrod) < 8:
      alert("Length of password must be greater than 8")
      return
    if self.passwrod != self.confirm_password:
      alert("Password and Confirm Paswword must be same")
      return
    pass
