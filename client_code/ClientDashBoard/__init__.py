from ._anvil_designer import ClientDashBoardTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ClientDashBoard(ClientDashBoardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.plot_1.figure = anvil.server.call('get_ratings_chart')
    self.plot_2.figure = anvil.server.call('get_competitor_plot')
    self.plot_3.figure = anvil.server.call('get_reviews_chart')

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
