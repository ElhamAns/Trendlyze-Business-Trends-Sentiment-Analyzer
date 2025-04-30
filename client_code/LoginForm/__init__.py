from ._anvil_designer import LoginFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users

from ..PaymentForm import PaymentForm
from ..SuccessPayment import SuccessPayment
from ..signUpReqquestStatus import signUpReqquestStatus
from datetime import datetime, timedelta




class LoginForm(LoginFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)


    self.links = [self.button_2, self.button_1]
    self.button_7.tag.url_hash = "home"
    self.button_2.tag.url_hash = "login"
    self.button_6.tag.url_hash = "home"
    self.button_1.tag.url_hash = "register"
    self.button_3.tag.url_hash = "payment"
    self.button_4.tag.url_hash = "success"


  def home_link_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_3.scroll_into_view(smooth=True)

  def button_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_5.scroll_into_view(smooth=True)

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("RegisterForm")
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("login")
    pass

  def button_5_click(self, **event_args):
    open_form('Form1')

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_12.scroll_into_view(smooth=True)

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_24.scroll_into_view(smooth=True)

  def button_8_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("PrivacyPolicy")

  def register_open(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('RegisterForm')
    pass

  def forget_password_open(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ForgetPasswordForm')
    pass

  def login_button(self, **event_args):
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
            anvil.server.call('get_session_unauthenticated')
            anvil.users.logout()
            open_form('LoginForm')
            return
        if user['deleted_at'] and user['deleted_at'] + timedelta(days=30) < datetime.now(anvil.tz.tzutc()):
          alert("Your account is deleted permanently please register again!")
          anvil.server.call('get_session_unauthenticated')
          anvil.users.logout()
          open_form('RegisterForm')
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

  def policy_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ServicePage')

  def privacy_statement_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('PrivacyPolicy')