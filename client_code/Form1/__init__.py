from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users

from ..Form1t import Form1t
from ..login import login
from ..register import register
from ..PaymentForm import PaymentForm
from ..SuccessPayment import SuccessPayment

# from anvil_extras import routing


# @routing.main_router
class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    
    self.init_components(**properties)
    
    # open_form('Form1t')
    
    self.links = [self.button_2, self.button_1]
    self.button_7.tag.url_hash  = 'home'
    self.button_2.tag.url_hash = 'login'
    self.button_6.tag.url_hash = 'home'
    self.button_1.tag.url_hash   = 'register'
    self.button_3.tag.url_hash   = 'payment'
    self.button_4.tag.url_hash   = 'success'

    # Any code you write here will run when the form opens.
  def home_link_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_3.scroll_into_view(smooth=True)

  def button_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_5.scroll_into_view(smooth=True)

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('RegisterForm')
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('LoginForm')
    pass

  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.card_1.scroll_into_view(smooth=True)
  
  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_12.scroll_into_view(smooth=True)

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_24.scroll_into_view(smooth=True)

  def button_8_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('PrivacyPolicy')

  def nav_link_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

