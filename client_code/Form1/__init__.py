from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users

class Form1(Form1Template):

  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)


    # Any code you write here will run when the form opens.
  def button_7_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_3.scroll_into_view(smooth=True)

  def button_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_5.scroll_into_view(smooth=True)

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

