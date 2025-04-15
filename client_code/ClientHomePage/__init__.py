from ._anvil_designer import ClientHomePageTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from plotly import graph_objects as go
import re



class ClientHomePage(ClientHomePageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.current_client = anvil.server.call('get_current_client')
    self.init_components(**properties)
    if self.current_client['shop']:
      self.plot_1.figure = anvil.server.call('get_home_page_rating', self.current_client['shop']['shop_name'])
    else:
      self.plot_1.figure = anvil.server.call('get_ratings_chart')
    self.label_5.text = f"Welcome Back {self.current_client['business_name']}"
    self.label_6.text = self.current_client['business_name']
    self.label_4.text = self.current_client['business_name']
    self.image_3.source = self.current_client['logo']
    self.label_3.text = self.current_client['description']
    
    self.repeating_panel_1.items = anvil.server.call('get_client_compitetors', self.current_client)
    # Any code you write here will run when the form opens.

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    response = alert("Are you sure you want to Logout?", buttons=["Yes", "No"])
    if response == "Yes":
      open_form('Rating')
      # alert("Users logged out successfully")

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ClientDashBoard')

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ClientSettings')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ClientDashBoard')

  def button_6_click(self, **event_args):
    text = self.text_area_1.text
    arabic_pattern = re.compile(r'^[\u0600-\u06FF\s]+$')
    
    if text and not arabic_pattern.match(text):
        alert("❌ Please enter Arabic text only. No English, numbers, or symbols allowed.")
    else:
        satisfaction = anvil.server.call('predict_sentiment',text)
        self.label_8.visible=True
        if satisfaction == 2:
          self.label_8.text = "Satisfied 😃"
        elif satisfaction == 1:
          self.label_8.text = "Partially Satisfied 😕"
        else:
          self.label_8.text = "Dissatisfied 😠"



