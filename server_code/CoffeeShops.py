import anvil.files
from anvil.files import data_files
import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.pdf
from anvil.pdf import PDFRenderer


# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def get_all_coffee_shop(first_six=False):
  if first_six:
    coffee_shops = app_tables.shops.search(anvil.tables.order_by('reviews_count', ascending=False))
    return [coffee_shop['shop_name'] for coffee_shop in coffee_shops[:6]]
  coffee_shops = app_tables.shops.search(tables.order_by('shop_name'))
  return [coffee_shop['shop_name'] for coffee_shop in coffee_shops]

@anvil.server.callable
def create_zaphod_pdf(cofee_shop=None, general_year=None, top_shop_name=None, start_year=None, end_year=None):
  media_object = PDFRenderer(filename="Dashboard").render_form('Report', coffee_name=cofee_shop, general_year=general_year, top_shop=top_shop_name, start_year=start_year, end_year=end_year)
  return media_object