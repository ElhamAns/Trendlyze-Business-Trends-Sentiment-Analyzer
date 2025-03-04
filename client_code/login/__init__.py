from ._anvil_designer import loginTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import anvil


class login(loginTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('register')
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('forgetPassword')
    pass
