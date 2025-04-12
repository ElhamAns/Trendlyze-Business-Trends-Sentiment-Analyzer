from ._anvil_designer import Form1tTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from anvil_extras import routing

@routing.route('home', title='Home | RoutingExample')  #multiple decorators allowed
@routing.route('',     title='Home | RoutingExample')
class Form1t(Form1tTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
