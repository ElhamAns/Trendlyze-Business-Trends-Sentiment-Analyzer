from ._anvil_designer import forgetPasswordTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server


class forgetPassword(forgetPasswordTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('_send_password_reset', self.text_box_2.text)
    alert(f'Forget password mail is sent, please check email {self.text_box_2.text}')
    open_form('Form1')
