from ._anvil_designer import ServicePageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil_extras import routing


class ServicePage(ServicePageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def nav_link_click(self, **event_args):
    """This method is called when a navigation link is clicked"""
    url_hash = event_args['sender'].tag.url_hash
    routing.set_url_hash(url_hash)

  def on_navigation(self, **nav_args):
    for link in self.links:
      link.role = 'selected' if link.tag.url_hash == nav_args['url_hash'] else ''

