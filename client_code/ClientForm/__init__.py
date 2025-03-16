from ._anvil_designer import ClientFormTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ClientForm(ClientFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.repeating_panel_1.items = anvil.server.call('get_all_clients')

    # Any code you write here will run when the form opens.
