from ._anvil_designer import RegisterFormTemplate
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
from ..signUpReqquestStatus import signUpReqquestStatus
from datetime import datetime, timedelta


# from anvil_extras import routing


# @routing.main_router
class RegisterForm(RegisterFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.

    self.init_components(**properties)

    # open_form('Form1t')

    self.links = [self.button_2, self.button_1]
    self.button_7.tag.url_hash = "home"
    self.button_2.tag.url_hash = "login"
    self.button_6.tag.url_hash = "home"
    self.button_1.tag.url_hash = "register"
    self.button_3.tag.url_hash = "payment"
    self.button_4.tag.url_hash = "success"

    # Any code you write here will run when the form opens.

  def home_link_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_3.scroll_into_view(smooth=True)

  def button_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Form1')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("RegisterForm")
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("login")
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

  def button_8_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("PrivacyPolicy")


  def open_login(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('LoginForm')

  def submit_button(self, **event_args):
    recaptcha_response = anvil.js.window.grecaptcha.getResponse()
    
    if not recaptcha_response:
        alert("Please complete the reCAPTCHA!")
        return
    
    # Verify the reCAPTCHA response
    verification = anvil.server.call('verify_recaptcha', recaptcha_response)
    
    if not verification.get('success', False):
        alert("reCAPTCHA verification failed. Please try again.")
        return
    mandatory_fields = {
        "Logo": self.file_loader_1.file,
        "Business name": self.business_name.text,
        "Email": self.email.text,
        "Confirm email": self.confirm_email.text,
        "Password": self.passwrod.text,
        "Confirm password": self.confirm_password.text,
        "Business type": self.type_drop_down.selected_value,
        "Country": self.country_drop_down.selected_value,
        "City": self.city_drop_down.selected_value,
        "Area": self.area_drop_down.selected_value,
        "Business description": self.text_area_1.text
    }
    
    missing_fields = [field_name for field_name, value in mandatory_fields.items() if not value]
    if missing_fields:
        alert(f"Please fill all mandatory fields: {', '.join(missing_fields)}")
        return
    
    # Email validation
    if self.email.text != self.confirm_email.text:
        alert("Email and Confirm email must be same")
        return
    
    # Password length validation
    if len(self.passwrod.text) < 8:
        alert("Password must be at least 8 characters long")
        return
    
    # Password complexity validation
    password = self.passwrod.text
    has_letter = any(c.isalpha() for c in password)
    has_number = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)
    
    if not (has_letter and has_number and has_symbol):
        alert("Password must contain at least 1 letter, 1 number, and 1 symbol")
        return
    
    # Password match validation
    if self.passwrod.text != self.confirm_password.text:
        alert("Password and Confirm Password must be same")
        return
    
    # Check if user already exists
    user_already_exist = anvil.server.call('check_existing_user', self.email.text)
    if user_already_exist:
        alert("User Already Exist")
        return
    
    # Proceed with signup
    err = anvil.server.call('_do_signup', 
                          self.file_loader_1.file, 
                          self.business_name.text, 
                          self.email.text, 
                          self.passwrod.text, 
                          self.type_drop_down.selected_value, 
                          self.country_drop_down.selected_value, 
                          self.city_drop_down.selected_value, 
                          self.area_drop_down.selected_value, 
                          self.text_area_1.text)
    
    if err is not None:
        alert(err)
    else:
        alert(f"We have sent a confirmation email to {self.email.text}.\n\nCheck your email, and click on the link.")
        open_form('LoginForm')
        return

    
  def enable_submit_button(self):
    if self.check_box_1.checked:
      print("in if")
      return True

  def check_box_1_change(self, **event_args):
    if self.check_box_1.checked:
      self.button_1.enabled = True
    else:
      self.button_1.enabled = False

  def check_box_2_change(self, **event_args):
    recaptcha_response = anvil.js.window.grecaptcha.getResponse()
    
    if not recaptcha_response:
        alert("Please complete the reCAPTCHA!")
        return
    
    # Verify the reCAPTCHA response
    verification = anvil.server.call('verify_recaptcha', recaptcha_response)
    
    if not verification.get('success', False):
        alert("reCAPTCHA verification failed. Please try again.")
        return

  def policy_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ServicePage')

  def privacy_statement_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('PrivacyPolicy')