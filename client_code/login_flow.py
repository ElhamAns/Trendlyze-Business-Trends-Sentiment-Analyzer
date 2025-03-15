import anvil
from anvil import alert
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .PasswordResetDialog import PasswordResetDialog

def do_email_confirm_or_reset():
  """Check whether the user has arrived from an email-confirmation link or a password reset, and pop up any necessary dialogs.
     Call this function from the 'show' event on your startup form.
  """
  h = anvil.get_url_hash()
  if isinstance(h, dict) and 'email' in h:
    if 'pwreset' in h:
      if not anvil.server.call('_is_password_key_correct', h['email'], h['pwreset']):
        alert("This is not a valid password reset link")
        return

      while True:
        pwr = PasswordResetDialog()
        if not alert(pwr, title="Reset Your Password", buttons=[("Reset password", True, 'primary'), ("Cancel", False)]):
          return
        if pwr.pw_box.text != pwr.pw_repeat_box.text:
          alert("Passwords did not match. Try again.")
        else:
          break
  
      if anvil.server.call('_perform_password_reset', h['email'], h['pwreset'], pwr.pw_box.text):
        alert("Your password has been reset. You are now logged in.")
      else:
        alert("This is not a valid password reset link")

        
    elif 'confirm' in h:
      if anvil.server.call('_confirm_email_address', h['email'], h['confirm']):
        alert("Thanks for confirming your email address. You are now logged in.")
        
      else:
        alert("This confirmation link is not valid. Perhaps you have already confirmed your address?\n\nTry logging in normally.")
