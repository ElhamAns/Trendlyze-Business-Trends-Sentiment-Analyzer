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
    print("in signup: ", self.item)
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

