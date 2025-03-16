from ._anvil_designer import ItemTemplate3Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
import anvil.tz


class ItemTemplate3(ItemTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  def get_time_difference(self):
    now = datetime.now(anvil.tz.tzlocal())

    # Calculate the time difference
    delta = now - self.item['created_at']

    # Get the total number of seconds
    seconds = delta.total_seconds()

    # Check for years, months, days, hours, minutes, and seconds
    years = seconds // (365.25 * 24 * 3600)
    if years >= 1:
        return f"{int(years)} year{'s' if years > 1 else ''} ago"
    
    months = seconds // (30.44 * 24 * 3600)  # Average month length in days
    if months >= 1:
        return f"{int(months)} month{'s' if months > 1 else ''} ago"
    
    days = seconds // (24 * 3600)
    if days >= 1:
        return f"{int(days)} day{'s' if days > 1 else ''} ago"
    
    hours = seconds // 3600
    if hours >= 1:
        return f"{int(hours)} hour{'s' if hours > 1 else ''} ago"
    
    minutes = seconds // 60
    if minutes >= 1:
        return f"{int(minutes)} minute{'s' if minutes > 1 else ''} ago"
    
    return f"{int(seconds)} { 'Just Now' if seconds < 40 else {seconds}} ago"

    