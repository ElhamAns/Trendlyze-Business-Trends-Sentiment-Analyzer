import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import open_form
from . import login_flow
from .Form1 import Form1

from anvil_extras import routing

routing.launch()
# login_flow.do_email_confirm_or_reset()
# open_form('Form1')