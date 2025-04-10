from ._anvil_designer import forgetPasswordTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from ..PasswordResetDialog import PasswordResetDialog


class forgetPassword(forgetPasswordTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
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
        open_form('login')
    else:
        alert("Password reset failed. Please try the process again.")

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('login')
