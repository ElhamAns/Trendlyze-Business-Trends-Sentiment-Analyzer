from ._anvil_designer import registerTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server


class register(registerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.type_drop_down.items = ['Pakistan', 'Sudia Arabia', 'UAE']
    self.country_drop_down.items = ['Pakistan', 'Sudia Arabia', 'UAE']
    self.city_drop_down.items = ['Pakistan', 'Sudia Arabia', 'UAE']
    self.area_drop_down.items = ['Pakistan', 'Sudia Arabia', 'UAE']

    # Any code you write here will run before the form opens.

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('login')
    pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.email.text != self.confirm_email.text:
      alert("Email and Confirm email must be same")
      return
    if len(self.passwrod.text) < 8:
      alert("Length of password must be greater than 8")
      return
    if self.passwrod.text != self.confirm_password.text:
      alert("Password and Confirm Paswword must be same")
      return
    user_already_exist = anvil.server.call('check_existing_user', self.email.text)
    if user_already_exist:
      alert("User Already Exist")
      return
    err = anvil.server.call('_do_signup', self.file_loader_1.file, self.business_name.text, self.email.text, self.passwrod.text, self.type_drop_down.selected_value, self.country_drop_down.selected_value, self.city_drop_down.selected_value, self.area_drop_down.selected_value, self.text_area_1.text)
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
