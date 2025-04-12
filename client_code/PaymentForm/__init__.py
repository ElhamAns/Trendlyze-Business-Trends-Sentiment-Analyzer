from ._anvil_designer import PaymentFormTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js


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
    open_form("ClientHomePage")

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("ClientDashBoard")

  def button_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.radio_button_2.selected:
      amount = 50
    elif self.radio_button_3.selected:
      amount=120
    else:
      alert("Select your payment Plan")
      return
    result = anvil.server.call('create_payment', amount=amount, description="Your product/service")
    
    if result['status'] == 'success':
        # Redirect to PayPal for payment
        anvil.js.window.location.href = result['approval_url']
    else:
        alert(f"Error creating payment: {result['message']}")

  def handle_navigation(url, **kwargs):
    if url.contains("/payment-cancelled"):
        # Extract the reason from query parameters
        reason = kwargs.get('reason', 'Payment was cancelled')
        # Open the cancelled form with the reason
        return PaymentCancelledForm(cancellation_reason=reason)



