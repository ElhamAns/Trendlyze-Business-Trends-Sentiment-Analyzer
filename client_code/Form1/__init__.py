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

from anvil_extras import routing


@routing.main_router
class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.links = [self.button_2, self.button_1]
    self.button_7.tag.url_hash  = 'home'
    self.button_2.tag.url_hash = 'login'
    self.button_1.tag.url_hash   = 'register'
    self.button_3.tag.url_hash   = 'payment'
    self.button_4.tag.url_hash   = 'success'

  def nav_link_click(self, **event_args):
    """This method is called when a navigation link is clicked"""
    url_hash = event_args['sender'].tag.url_hash
    routing.set_url_hash(url_hash)

  def on_navigation(self, **nav_args):
    # this method is called whenever routing navigates to a new url
    # an example of setting the link as selected 
    # depending on the url_hash that is being navigated to
    for link in self.links:
      link.role = 'selected' if link.tag.url_hash == nav_args['url_hash'] else ''

    # Any code you write here will run when the form opens.
  def home_link_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_3.scroll_into_view(smooth=True)

  def button_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.raise_event_on_children(self.label_5.scroll_into_view(smooth=True))

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('register')
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('login')
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

