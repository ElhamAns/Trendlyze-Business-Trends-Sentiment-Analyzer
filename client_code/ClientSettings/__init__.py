from ._anvil_designer import ClientSettingsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ClientSettings(ClientSettingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.current_client = anvil.server.call('get_current_client')
    self.init_components(**properties)
    self.label_1.text = f"Welcome, {self.current_client['business_name']}"
    self.label_4.text = f"{self.current_client['business_name']} User"
    self.label_2.text = f"{self.current_client['business_name']}"
    self.label_8.text = f"{self.current_client['user']['email']}"
    self.image_2.source = self.current_client['logo']
    self.image_3.source = self.current_client['logo']
    

    # Any code you write here will run when the form opens.

  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ClientHomePage')

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ClientDashBoard')
