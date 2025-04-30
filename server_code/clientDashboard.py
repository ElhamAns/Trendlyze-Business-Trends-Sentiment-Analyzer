import anvil.files
from anvil.files import data_files
import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from collections import Counter

@anvil.server.callable
def get_client_home_page(user_client):

    # client_name = user_client['business_name']

    # # Pull just the reviews with label=2
    # reviews = app_tables.reviews.search(label=2)

    # shop_names = []
    # for review in reviews:
    #     shop_row = review['shop']
    #     if not shop_row:
    #         continue  # skip if no shop linked

    #     # Only fetch shop_name once
    #     shop_name = shop_row['shop_name']
    #     if shop_name and shop_name != client_name:
    #         shop_names.append(shop_name)

    # Use Counter to find top 4
    # return Counter(shop_names).most_common(4)
    return [("Barn's | بارنز", 109), ('Dose Cafe', 93), ('ZOYA COFFEE I مقهى زويا', 91), ('DYJOR Coffee Roasters', 89)]



@anvil.server.callable
def get_client_compitetors(user_client):
  search_results = app_tables.shops.search(shop_name=q.not_(user_client['business_name']))
  final_result = []
  number = 0
  for result in search_results:
    number+=1
    final_result.append({"No": number, "row": result})
  return final_result


