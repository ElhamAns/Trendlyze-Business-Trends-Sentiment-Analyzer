from ._anvil_designer import ClientSettingsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta
import anvil.tz

class ClientSettings(ClientSettingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.current_client = anvil.server.call('get_current_client')
    self.label_1.text = f"Welcome, {self.current_client['business_name']}"
    self.label_4.text = f"{self.current_client['business_name']} User"
    self.label_2.text = f"{self.current_client['business_name']}"
    self.label_8.text = f"{self.current_client['user']['email']}"
    self.image_2.source = self.current_client['logo']
    self.image_3.source = self.current_client['logo']
    self.type_drop_down.items = ['Coffee Shop']
    self.country_drop_down.items = ['Saudi Arabia']
    self.city_drop_down.items = ['Al-Khobar']
    self.area_drop_down.items = ['North Alkhobar', 'West Alkhobar', 'South Alkhobar', 'Rakah','Thoqbah']
    self.text_box_1.text = self.current_client['business_name']
    self.type_drop_down.selected_value = self.current_client['business_type']
    self.country_drop_down.selected_value = self.current_client['country']
    self.city_drop_down.selected_value = self.current_client['city']
    self.area_drop_down.selected_value = self.current_client['area']
    self.label_12.text = self.current_client['subscription_package']['type']
    self.init_components(**properties)
    

    # Any code you write here will run when the form opens.

  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    if (self.current_client['subsribed_at']+ timedelta(days=self.current_client['subscription_package']['time_period'])) <  datetime.now(anvil.tz.tzutc()):
        alert("Your subscription ended please pay again to use this app")
    else:
      open_form("ClientDashBoard")

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    if (self.current_client['subsribed_at']+ timedelta(days=self.current_client['subscription_package']['time_period'])) <  datetime.now(anvil.tz.tzutc()):
        alert("Your subscription ended please pay again to use this app")
    else:
      open_form("ClientDashBoard")
  def button_7_click(self, **event_args):
    """This method is called when the button is clicked"""
    response = alert("""Note: your account will be deleted permanently after 30 days. If you tried to login into
your account within 30 days, your account will be reactivated.Are you sure you want to delete your profile?""", buttons=["Yes", "No"])
    if response == "Yes":
        anvil.server.call('delete_user_account')
        alert("Your profile has been deleted.")
        anvil.server.session["authenticated"] = False
        anvil.users.logout()
        open_form('LoginForm')

  def button_8_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ForgetPasswordForm')

  def button_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    if not self.text_box_1.text or self.text_box_1.text == " ":
      alert("Business Name Cannot be Empty")
      return
    edited = anvil.server.call('edit_profile', self.text_box_1.text, self.type_drop_down.selected_value, self.country_drop_down.selected_value, self.city_drop_down.selected_value, self.area_drop_down.selected_value)
    if edited:
      self.refresh_data_bindings()
      self.current_client = anvil.server.call('get_current_client')
      self.label_2.text = self.current_client['business_name']
      self.label_4.text = f"{self.current_client['business_name']} User"
      self.label_1.text = f"Welcome, {self.current_client['business_name']}"
      alert("Your profile is edited successfully")
    else:
      alert("You don't have any thing to edit")

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('PaymentForm')

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    response = alert("Are you sure you want to Logout?", buttons=["Yes", "No"])
    if response == "Yes":
      anvil.server.call('get_session_unauthenticated')
      anvil.users.logout()
      alert("Users logged out successfully")
      open_form('HomePage')

  def policy_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ServicePage')

  def privacy_statement_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('PrivacyPolicy')
    
