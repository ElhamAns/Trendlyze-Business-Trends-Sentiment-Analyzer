from ._anvil_designer import extra_form1Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class extra_form1(extra_form1Template):
  def __init__(self, **properties):
    self.card_1.scroll_into_view(smooth=True)
    self.init_components(**properties)
    self.card_1.scroll_into_view(smooth=True)

  def handle_click(self, **event_args):
    alert("The button got clicked!")

