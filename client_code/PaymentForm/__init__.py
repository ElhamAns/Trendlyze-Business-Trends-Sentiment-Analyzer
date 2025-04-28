from ._anvil_designer import PaymentFormTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
from datetime import datetime, timedelta
import anvil.tz

from anvil_extras import routing

@routing.route('payment', title="BusinessTrend")
@routing.route('cancel-payment', url_keys=['token', routing.ANY], title="cancel-payment | PaymentForm")
class PaymentForm(PaymentFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.current_client = anvil.server.call("get_current_client")
    self.label_1.text = f"Welcome, {self.current_client['business_name']}"
    self.label_4.text = f"{self.current_client['business_name']} User"
    self.label_2.text = f"{self.current_client['business_name']}"
    self.label_8.text = f"{self.current_client['user']['email']}"
    self.image_2.source = self.current_client["logo"]
    self.image_3.source = self.current_client["logo"]
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    if not self.current_client['subsribed_at']:
      alert("Please Subsribe First to use this app")
      return
    if (self.current_client['subsribed_at']+ timedelta(days=self.current_client['subscription_package']['time_period'])) <  datetime.now(anvil.tz.tzutc()):
        alert("Your subscription ended please pay again to use this app")
    else:
      open_form("ClientDashBoard")

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    if not self.current_client['subsribed_at']:
      alert("Please Subsribe First to use this app")
      return
    if not self.current_client['subsribed_at'] and (self.current_client['subsribed_at']+ timedelta(days=self.current_client['subscription_package']['time_period'])) <  datetime.now(anvil.tz.tzutc()):
        alert("Your subscription ended please pay again to use this app")
    else:
      open_form("ClientDashBoard")

  def button_6_click(self, **event_args):
    if self.current_client['subscription_package'] and self.current_client['subscription_package']['type'] == 'Trial' and self.radio_button_1.selected:
      alert("You already subscibed Trail plan you can't select trail plan again")
      return
    """This method is called when the button is clicked"""
    if self.radio_button_1.selected:
      anvil.server.call('update_users_trail_payment')
      alert("Trail Plan in activated Successfully!")
      open_form('ClientHomePage')
      return
    if self.radio_button_2.selected:
      amount = 50
    elif self.radio_button_3.selected:
      amount=120
    else:
      alert("Select your payment Plan")
      return
    result = anvil.server.call('create_payment', amount=amount, description="Subscription Payment for Business Trend")
    
    if result['status'] == 'success':
        anvil.js.window.location.href = result['approval_url']
    else:
        alert(f"Error creating payment: {result['message']}")

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    response = alert("Are you sure you want to Logout?", buttons=["Yes", "No"])
    if response == "Yes":
      anvil.server.call('get_session_unauthenticated')
      anvil.users.logout()
      alert("Users logged out successfully")
      open_form('Form1')

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ClientSettings')

  def policy_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ServicePage')

  def privacy_statement_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('PrivacyPolicy')



