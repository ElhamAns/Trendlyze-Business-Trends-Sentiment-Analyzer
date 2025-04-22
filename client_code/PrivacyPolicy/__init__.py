from ._anvil_designer import PrivacyPolicyTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil_extras import routing


@routing.route('privacyPolicy', title="BusinessTrend")
class PrivacyPolicy(PrivacyPolicyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.links = [self.button_2, self.button_1, self.button_6]
    self.button_7.tag.url_hash  = 'home'
    self.button_2.tag.url_hash = 'login'
    self.button_6.tag.url_hash = 'home'
    self.button_1.tag.url_hash   = 'register'


  def nav_link_click(self, **event_args):
    """This method is called when a navigation link is clicked"""
    url_hash = event_args['sender'].tag.url_hash
    routing.set_url_hash(url_hash)

  def on_navigation(self, **nav_args):
    for link in self.links:
      link.role = 'selected' if link.tag.url_hash == nav_args['url_hash'] else ''

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('register')
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('login')
    pass