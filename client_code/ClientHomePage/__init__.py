from ._anvil_designer import ClientHomePageTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from plotly import graph_objects as go


class ClientHomePage(ClientHomePageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.plot_1.layout.plot_bgcolor='rgba(0,0,0,0)'  # Transparent plot background
    # paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
# )
    self.plot_1.data = go.Pie(
      labels=['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen'],
      values=[4500, 2500, 1053, 500],
      paper_bgcolor='rgba(0,0,0,0)',
      hole=.5,
      width=800,
    )
    self.plot_1.layout={
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
'width': 1200,
}

    # Any code you write here will run when the form opens.
