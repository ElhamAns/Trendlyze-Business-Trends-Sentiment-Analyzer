from ._anvil_designer import SuccessPaymentTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js

from anvil_extras import routing

@routing.route('success', title="BusinessTrend")
@routing.route(
  "success-payment",
  url_keys=["token", routing.ANY],
  title="cancel-payment | CancelPayment",
)
class SuccessPayment(SuccessPaymentTemplate):
  def __init__(self, **properties):
    anvil.server.call('update_user_payment', self.url_dict['token'])
    
