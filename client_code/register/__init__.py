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
