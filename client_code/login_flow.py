import anvil
from anvil import alert
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .PasswordResetDialog import PasswordResetDialog
from .signUpReqquestStatus import signUpReqquestStatus
from datetime import datetime, timedelta
import anvil.tz

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
  
      if anvil.server.call('_perform_password_reset', h['email'], pwr.pw_box.text):
        alert("Your password has been reset. You are now logged in.")
      else:
        alert("This is not a valid password reset link")

        
    elif 'confirm' in h:
      if anvil.server.call('_confirm_email_address', h['email'], h['confirm']):
        alert("Thanks for confirming your email address. You are now logged in.")
        
      else:
        alert("This confirmation link is not valid. Perhaps you have already confirmed your address?\n\nTry logging in normally.")

  
  user = anvil.users.get_user()
  if anvil.server.call('get_authticated_session'):
    anvil.server.call('get_session_authenticated')
    print("here")
    if user:
      print("in session auth")
      if user['is_admin']:
        anvil.open_form('admin_dashboard')
        return
      if user['deleted_at'] and user['deleted_at'] + timedelta(days=30) > datetime.now(anvil.tz.tzutc()):
        response = alert("Your account is deleted, do you want to reactivate your account?", buttons=["Yes", "No"])
        if response == "Yes":
          anvil.server.call('reactivate_deleted_account')
          alert("Your account is reactivated succesfully Login you use Business Trend Again!")
          anvil.open_form('LoginForm')
          return
      if user['deleted_at'] and user['deleted_at'] + timedelta(days=30) < datetime.now(anvil.tz.tzutc()):
        alert("Your account is deleted permanently please register again!")
        anvil.open_form('RegisterForm')
        return
      client = app_tables.clients.get(user=user)
      if not client['status']:
        anvil.open_form(signUpReqquestStatus(item=client))
        return
      elif not client['subscription_package']:
        anvil.open_form(signUpReqquestStatus(item=client))
        return
      elif client['subscription_package'] and (client['subsribed_at']+ timedelta(days=client['subscription_package']['time_period'])) > datetime.now(anvil.tz.tzutc()):
        anvil.open_form('ClientHomePage')
      elif (client['subsribed_at']+ timedelta(days=client['subscription_package']['time_period'])) <  datetime.now(anvil.tz.tzutc()):
        anvil.open_form('PaymentForm')
        alert("Your subscription ended please pay again to use this app")
      else:
        anvil.open_form(signUpReqquestStatus(item=client))
