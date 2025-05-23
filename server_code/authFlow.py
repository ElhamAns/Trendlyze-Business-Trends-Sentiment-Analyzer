import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
import sys
from anvil.tables import app_tables
import anvil.server
from anvil.http import url_encode
import bcrypt
from random import SystemRandom
from datetime import datetime
from login import login
random = SystemRandom()

def mk_token():
  """Generate a random 14-character token"""
  return "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789") for i in range(14)])

@anvil.server.callable
def _send_password_reset(email):
  """Send a password reset email to the specified user"""
  user = app_tables.users.get(email=email)
  if user is not None:
    user['link_key'] = mk_token()
    anvil.email.send(to=user['email'], subject="Reset your password", text=f"""
Hi,

Someone has requested a password reset for your account. If this wasn't you, just delete this email.
If you do want to reset your password, click here:

{anvil.server.get_app_origin('published')}#?email={url_encode(user['email'])}&pwreset={url_encode(user['link_key'])}

Thanks!
""")
    return True


@anvil.server.callable
def _send_email_confirm_link(email):
  """Send an email confirmation link if the specified user's email is not yet confirmed"""
  user = app_tables.users.get(email=email)
  if user is not None and not user['confirmed_email']:
    if user['link_key'] is None:
      user['link_key'] = mk_token()
    anvil.email.send(to=user['email'], subject="Confirm your email address", text=f"""
Hi,

Thanks for signing up for our service. To complete your sign-up, click here to confirm your email address:

{anvil.server.get_app_origin('published')}#?email={url_encode(user['email'])}&confirm={url_encode(user['link_key'])}

Thanks!
""")
    return True

def hash_password(password, salt):
  """Hash the password using bcrypt in a way that is compatible with Python 2 and 3."""
  if not isinstance(password, bytes):
    password = password.encode()
  if not isinstance(salt, bytes):
    salt = salt.encode()

  result = bcrypt.hashpw(password, salt)

  if isinstance(result, bytes):
    return result.decode('utf-8')


@anvil.server.callable
def _do_signup(logo, business_name, email, password, business_type, country, city, area, description):
  
  pwhash = hash_password(password, bcrypt.gensalt())
  
  # Add the user in a transaction, to make sure there is only ever one user in this database
  # with this email address. The transaction might retry or abort, so wait until after it's
  # done before sending the email.

  @tables.in_transaction
  def add_user_if_missing():
    user = app_tables.users.get(email=email)
    if user is None:
      user = app_tables.users.add_row(logo=logo, 
                           business_name=business_name, 
                           email=email, 
                           password_hash=pwhash, 
                           business_type=business_type, 
                           country=country, 
                           city=city, 
                           area=area, 
                           description=description,
                           requested_at=datetime.now(),
                           # will remove this on email send
                           enabled=True
                                )
      return user
    
  user = add_user_if_missing()

  if user is None:
    return "This email address has already been registered for our service. Try logging in."
  
  # _send_email_confirm_link(email)
  
  # No error = success
  return None
  
    
def get_user_if_key_correct(email, link_key):
  user = app_tables.users.get(email=email)

  if user is not None and user['link_key'] is not None:
    # Use bcrypt to hash the link key and compare the hashed version.
    # The naive way (link_key == user['link_key']) would expose a timing vulnerability.
    salt = bcrypt.gensalt()
    if hash_password(link_key, salt) == hash_password(user['link_key'], salt):
      return user


@anvil.server.callable
def _is_password_key_correct(email, link_key):
  return get_user_if_key_correct(email, link_key) is not None

@anvil.server.callable
def _perform_password_reset(email, reset_key, new_password):
  """Perform a password reset if the key matches; return True if it did."""
  user = get_user_if_key_correct(email, reset_key)
  if user is not None:
    user['password_hash'] = hash_password(new_password, bcrypt.gensalt())
    user['link_key'] = None
    anvil.users.force_login(user)
    return True
    
@anvil.server.callable
def _confirm_email_address(email, confirm_key):
  """Confirm a user's email address if the key matches; return True if it did."""
  user = get_user_if_key_correct(email, confirm_key)
  if user is not None:
    user['confirmed_email'] = True
    user['link_key'] = None
    user['enabled'] = True
    anvil.users.force_login(user)
    return True

@anvil.server.callable
def check_existing_user(email):
  user = app_tables.users.get(email=email, enabled=True)
  if user:
    return True


def login_with_form(allow_cancel=False):
  """Log in by popping up the custom LoginDialog"""
  d = login()

  BUTTONS = [("Log in", "login", "primary")]
  if allow_cancel:
    BUTTONS += [("Cancel", None)]
  
  while anvil.users.get_user() is None:
    choice = alert(d, title="Log In", dismissible=allow_cancel, buttons=BUTTONS)
    
    if choice == 'login':
      try:
        anvil.users.login_with_email(d.email_box.text, d.password_box.text, remember=True)
      except anvil.users.EmailNotConfirmed:
        d.confirm_lnk.visible = True
      except anvil.users.AuthenticationFailed as e:
        d.login_err_lbl.text = str(e.args[0])
        d.login_err_lbl.visible = True
        
    elif choice == 'reset_password':
      fp = ForgottenPasswordDialog(d.email_box.text)
      
      if alert(fp, title='Forgot Password', buttons=[("Reset password", True, "primary"), ("Cancel", False)]):
        
        if anvil.server.call('_send_password_reset', fp.email_box.text):
          alert(f"A password reset email has been sent to {fp.email_box.text}.")
        else:
          alert("That username does not exist in our records.")
        
    elif choice == 'confirm_email':
      if anvil.server.call('_send_email_confirm_link', d.email_box.text):
        alert(f"A new confirmation email has been sent to {d.email_box.text}.")
      else:
        alert(f"'{d.email_box.text}' is not an unconfirmed user account.")
      d.confirm_lnk.visible = False
    
    elif choice is None and allow_cancel:
      break