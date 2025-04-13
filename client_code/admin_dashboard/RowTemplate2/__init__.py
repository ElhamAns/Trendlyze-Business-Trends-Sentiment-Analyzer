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
    anvil.email.send(to=self.item['user']['email'], subject="Approved by Businnes Trend Admin",text=f"""
    You are approved! Please enter to complete the payment to
activate your account {anvil.server.get_app_origin('published')}
  Thanks!
  """ )
    self.refresh_data_bindings()

  def button_2_click(self, **event_args):
    self.item['status'] = False
    anvil.email.send(to=self.item['user']['email'], subject="Approved by Businnes Trend Admin",text="""We’re sorry to inform you that you have been rejected. Please
  contact us for further information Seniorprojectbtsa@gmail.com
  Thanks!
  """ )
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
    
