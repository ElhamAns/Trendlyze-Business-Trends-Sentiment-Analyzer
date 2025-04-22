from ._anvil_designer import Form1tTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# from anvil_extras import routing

# @routing.route('home', title='Home | Trendlyze')
# @routing.route('',     title='Home | Trendlyze')
class Form1t(Form1tTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.card_1.scroll_into_view(smooth=True)
    self.init_components(**properties)
    self.card_1.scroll_into_view(smooth=True)
    self.column_panel_3.add_event_handler('x-click', self.handle_click)

  def handle_click(self, **event_args):
    print("in here")
    alert("The button got clicked!")

    # Any code you write here will run before the form opens.
