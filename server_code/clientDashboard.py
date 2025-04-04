import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from collections import Counter

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
def get_client_home_page(user_client):
  
  client_name = user_client['business_name']
  client = app_tables.shops.get(shop_name=client_name)
  shops = app_tables.reviews.search(label=2, shop=q.not_(client))
  shop_name = [shop['shop']['shop_name'] for shop in shops]
  name_count = Counter(shop_name).most_common(4)
  return name_count

@anvil.server.callable
def get_client_compitetors(user_client):
  search_results = app_tables.shops.search(shop_name=q.not_(user_client['business_name']))
  final_result = []
  number = 0
  for result in search_results:
    number+=1
    final_result.append({"No": number, "row": result})
  return final_result


