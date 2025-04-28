from ._anvil_designer import RatingTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Rating(RatingTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('all_app_review', 1)
    anvil.server.call('get_session_unauthenticated')
    anvil.users.logout()
    alert("Users logged out successfully")
    open_form("Form1")

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('all_app_review', 2)
    anvil.server.call('get_session_unauthenticated')
    anvil.users.logout()
    alert("Users logged out successfully")
    open_form("Form1")

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('all_app_review', 3)
    anvil.server.call('get_session_unauthenticated')
    anvil.users.logout()
    alert("Users logged out successfully")
    open_form("Form1")

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('all_app_review', 4)
    anvil.server.call('get_session_unauthenticated')
    anvil.users.logout()
    alert("Users logged out successfully")
    open_form("Form1")

  def button_4_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('all_app_review', 5)
    anvil.server.call('get_session_unauthenticated')
    anvil.users.logout()
    alert("Users logged out successfully")
    open_form("Form1")
