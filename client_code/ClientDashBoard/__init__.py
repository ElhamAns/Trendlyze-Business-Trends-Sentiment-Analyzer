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
    self.drop_down_1.items = ["2025", "2024", "2023", "2022", "2021", "2020", "2019"]
    self.plot_1.figure = anvil.server.call('get_ratings_chart')
    self.drop_down_3.items = anvil.server.call('get_all_coffee_shop')
    self.plot_2.figure = anvil.server.call('get_total_review_counts')
    self.plot_3.figure = anvil.server.call('get_reviews_chart')

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    open_form('Form1')

  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ClientHomePage')
    
  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ClientSettings')

  def drop_down_3_change(self, **event_args):
    """This method is called when an item is selected"""
    self.plot_1.figure = anvil.server.call('get_home_page_rating', self.drop_down_3.selected_value)
    self.plot_2.figure = anvil.server.call('get_shop_reviews', self.drop_down_3.selected_value)
    self.plot_3.figure = anvil.server.call('get_shop_sentiments', self.drop_down_3.selected_value)

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    self.plot_2.figure = anvil.server.call('get_total_review_counts', year = self.drop_down_1.selected_value)
    
    
