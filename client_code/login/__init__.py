from ._anvil_designer import loginTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import anvil
from ..signUpReqquestStatus import signUpReqquestStatus


class login(loginTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('register')
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('forgetPassword')
    pass

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    try:
      user = anvil.users.login_with_email(self.email_text_box.text, self.password_text_box.text, remember=True)
      if user['is_admin']:
        open_form('admin_dashboard')
        return
      open_form(signUpReqquestStatus(item=user))
    except anvil.users.AuthenticationFailed as e:
      alert("user not found")
    # user = anvil.users.login_with_email(self.email_text_box, self.password_text_box)
    # if user:
    #   alert("user loged in successfully")
      
