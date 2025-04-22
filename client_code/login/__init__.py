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
      if user:
        anvil.server.call('get_session_authenticated')
      if anvil.server.call('get_authticated_session'):
        if user['is_admin']:
          open_form('admin_dashboard')
          return
        if user['deleted_at'] and user['deleted_at'] + timedelta(days=30) > datetime.now(anvil.tz.tzutc()):
          response = alert("Your account is deleted, do you want to reactivate your account?", buttons=["Yes", "No"])
          if response == "Yes":
            anvil.server.call('reactivate_deleted_account')
            alert("Your account is reactivated succesfully Login you use Business Trend Again!")
            anvil.users.logout()
            open_form('login')
            return
        if user['deleted_at'] and user['deleted_at'] + timedelta(days=30) < datetime.now(anvil.tz.tzutc()):
          alert("Your account is deleted permanently please register again!")
          anvil.users.logout()
          open_form('register')
          return
          
        client = anvil.server.call('get_user_cleint', user)
        if not client['status']:
          open_form(signUpReqquestStatus(item=client))
          return
        elif not client['subscription_package']:
          open_form(signUpReqquestStatus(item=client))
          return
        elif client['subscription_package'] and (client['subsribed_at']+ timedelta(days=client['subscription_package']['time_period'])) > datetime.now(anvil.tz.tzutc()):
          open_form('ClientHomePage')
        elif (client['subsribed_at']+ timedelta(days=client['subscription_package']['time_period'])) <  datetime.now(anvil.tz.tzutc()):
          open_form('PaymentForm')
          alert("Your subscription ended please pay again to use this app")
        else:
          open_form(signUpReqquestStatus(item=client))
    except anvil.users.AuthenticationFailed as e:
      alert(f"{e}")
    # user = anvil.users.login_with_email(self.email_text_box, self.password_text_box)
    # if user:
    #   alert("user loged in successfully")
      
