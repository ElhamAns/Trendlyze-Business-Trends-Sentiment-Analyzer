from ._anvil_designer import loginTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from datetime import datetime, timedelta
import anvil.tz
from ..signUpReqquestStatus import signUpReqquestStatus

from anvil_extras import routing

@routing.route('login', title="BusinessTrend")
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
      print("user: ", user)
      client = anvil.server.call('get_user_cleint', user)
      if not client['status']:
        open_form(signUpReqquestStatus(item=client))
      # if client['subscription_package'] and (client['subsribed_at']+ timedelta(days=client['subscription_package']['time_period'])) > datetime.now(anvil.tz.tzutc()):
      #   open_form('ClientHomePage')
      elif (client['subsribed_at']+ timedelta(days=client['subscription_package']['time_period'])) <  datetime.now(anvil.tz.tzutc()):
        alert("Your subscription ended please pay again to use this app")
        open_form('PaymentForm')
      else:
        open_form(signUpReqquestStatus(item=client))
    except anvil.users.AuthenticationFailed as e:
      alert(f"{e}")
    # user = anvil.users.login_with_email(self.email_text_box, self.password_text_box)
    # if user:
    #   alert("user loged in successfully")
      
