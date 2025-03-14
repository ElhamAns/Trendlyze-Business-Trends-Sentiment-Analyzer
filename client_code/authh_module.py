import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import open_form
from . import login_flow

login_flow.do_email_confirm_or_reset()
open_form('Form1')