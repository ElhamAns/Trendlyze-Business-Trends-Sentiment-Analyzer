from ._anvil_designer import ReviewsTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from plotly import graph_objects as go


class Reviews(ReviewsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.current_client = anvil.server.call("get_current_client")
    self.init_components(**properties)
    self.drop_down_1.items = ["All Reviews", "Satisfied", "Partially Satisfied", "Dissatisfied"]
    self.drop_down_2.items = ["All Reviews", "Service","Products","Price","Place"]
    self.label_4.text = self.current_client["business_name"]
    self.image_3.source = self.current_client["logo"]
    self.repeating_panel_1.items = anvil.server.call('get_client_reviews', shop_name=self.item)

    # Any code you write here will run when the form opens.

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    response = alert("Are you sure you want to Logout?", buttons=["Yes", "No"])
    if response == "Yes":
      open_form("Rating")
      # alert("Users logged out successfully")

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("ClientDashBoard")

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("ClientSettings")

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("ClientDashBoard")

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    self.drop_down_2.selected_value = "All Reviews"
    self.repeating_panel_1.items = anvil.server.call('get_client_reviews', shop_name=self.item, rating_filter=self.drop_down_1.selected_value)

  def drop_down_2_change(self, **event_args):
    """This method is called when an item is selected"""
    self.repeating_panel_1.items = anvil.server.call('get_client_review_type',self.item, self.drop_down_1.selected_value, self.drop_down_2.selected_value)

  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ClientHomePage')
