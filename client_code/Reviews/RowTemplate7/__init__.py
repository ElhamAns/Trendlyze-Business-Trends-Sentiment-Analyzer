from ._anvil_designer import RowTemplate7Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate7(RowTemplate7Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def review_rating(self):
    if self.item['label'] == 2:
      return "Satisfied 😄"
    elif self.item['label'] == 1:
      return "Partially Satisfied"
    return "Dissatisfied"

    # Any code you write here will run before the form opens.
