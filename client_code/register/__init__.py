from ._anvil_designer import registerTemplate
# from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server

from anvil_extras import routing

@routing.route('register', title="register | BusinessTrend")
class register(registerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.type_drop_down.items = ['Coffee Shop']
    self.country_drop_down.items = ['Saudia Arabia']
    self.city_drop_down.items = ['Al-Khobar']
    self.area_drop_down.items = ['North Alkhobar', 'West Alkhobar', 'South Alkhobar', 'Rakah','Thoqbah']

    # Any code you write here will run before the form opens.

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('login')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Check all mandatory fields are filled
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
        open_form('login')
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
