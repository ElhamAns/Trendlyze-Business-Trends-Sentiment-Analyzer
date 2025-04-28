from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
import anvil.email


class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)


  def button_1_click(self, **event_args):
    self.item['status'] = True
    print("here")
    anvil.server.call('send_approval_email',self.item['user']['email'], True)
    self.refresh_data_bindings()

  def button_2_click(self, **event_args):
    self.item['status'] = False
    anvil.server.call('send_approval_email',self.item['user']['email'], False)
    self.refresh_data_bindings()
    """This method is called when the button is clicked"""
    pass

  def get_status(self):
    if self.item['status']:
      return 'Accepted'
    elif self.item['status'] == False:
      return 'Rejected'
    else:
      return 'Pending'
    
