from ._anvil_designer import ForgetPasswordFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users

from ..PaymentForm import PaymentForm
from ..SuccessPayment import SuccessPayment

# from anvil_extras import routing


# @routing.main_router
class ForgetPasswordForm(ForgetPasswordFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.

    self.init_components(**properties)


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
    self.label_5.scroll_into_view(smooth=True)

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("RegisterForm")
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("LoginForm")
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

  def nav_link_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def policy_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("ServicePage")

  def privacy_statement_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("PrivacyPolicy")

  def send_otp_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Step 1: Send reset code
    email = self.text_box_2.text
    reset_code = anvil.server.call('_send_password_reset', email)
    
    if not reset_code:
        alert("The email you entered is not registered")
        return
    
    # Step 2: Verify OTP - keep asking until correct or cancelled
    while True:
        t = TextBox(placeholder="Enter 6-digit code")
        result = alert(content=t,
                     title="Verify Code",
                     buttons=[("Verify", True), ("Cancel", False)])
        
        if not result:  # User clicked Cancel
            return
        
        if not t.text:  # Empty code
            alert("Please enter the 6-digit code")
            continue
            
        if reset_code == t.text:  # Correct code
            break
            
        alert("The code you entered is incorrect. Please try again.")
    
    # Step 3: Password reset - keep asking until valid or cancelled
    while True:
        pwr = PasswordResetDialog()
        result = alert(pwr, 
                      title="Reset Your Password", 
                      buttons=[("Reset Password", True, 'primary'), ("Cancel", False)])
        
        if not result:  # User clicked Cancel
            return
        
        password = pwr.pw_box.text
        confirm_pw = pwr.pw_repeat_box.text
        
        # Validate password complexity
        has_letter = any(c.isalpha() for c in password)
        has_number = any(c.isdigit() for c in password)
        has_symbol = any(not c.isalnum() for c in password)
        
        # Check all requirements
        if len(password) < 8:
            alert("Password must be at least 8 characters")
            continue
            
        if not has_letter:
            alert("Password must contain at least 1 letter")
            continue
            
        if not has_number:
            alert("Password must contain at least 1 number")
            continue
            
        if not has_symbol:
            alert("Password must contain at least 1 symbol")
            continue
            
        if password != confirm_pw:
            alert("Passwords did not match. Try again.")
            continue
            
        # All validations passed - exit loop
        break
    
    # Perform the actual password reset
    if anvil.server.call('_perform_password_reset', email, password):
        alert("Your password has been reset successfully!")
        open_form('LoginForm')
    else:
        alert("Password reset failed. Please try the process again.")

  def login_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('LoginForm')
