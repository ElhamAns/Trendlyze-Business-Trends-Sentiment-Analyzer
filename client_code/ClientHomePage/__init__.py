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
    self.current_client = anvil.server.call('get_current_client')
    self.init_components(**properties)
    if self.current_client['shop']:
      self.plot_1.figure = anvil.server.call('get_home_page_rating')
    else:
      self.plot_1.figure = anvil.server.call('get_ratings_chart')
    self.label_5.text = f"Welcome Back {self.current_client['business_name']}"
    self.label_6.text = self.current_client['business_name']
    self.label_4.text = self.current_client['business_name']
    self.image_3.source = self.current_client['logo']
    if self.current_client['shop']:
      self.label_3.text = self.current_client['description']
    
    self.repeating_panel_1.items = anvil.server.call('get_client_compitetors', self.current_client)
    # Any code you write here will run when the form opens.

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    alert("Users logged out successfully")
    open_form('Form1')

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ClientDashBoard')

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ClientSettings')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ClientDashBoard')

