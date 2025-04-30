from ._anvil_designer import extraTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class extra(extraTemplate):
  def __init__(self, **properties):
    self.card_1.scroll_into_view(smooth=True)
    self.init_components(**properties)
    self.card_1.scroll_into_view(smooth=True)

  def handle_click(self, **event_args):
    alert("The button got clicked!")

