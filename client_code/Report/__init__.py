from ._anvil_designer import ReportTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Report(ReportTemplate):
  def __init__(self, coffee_name=None,general_year=None,top_shop=None, **properties):
    # Set Form properties and Data Bindings.
    self.first_coffee_shops = anvil.server.call('get_all_coffee_shop', True)
    if coffee_name:
      self.drop_down_1.items =  ["2025", "2024", "2023", "2022", "2021", "2020", "2019","2018", "2017", "2016", "2015", "2014" ]
      self.label_3.text = f"{coffee_name}"
      self.label_2.text = "Real Customer Sentiments"
      self.plot_1.figure = anvil.server.call('get_home_page_rating', coffee_name)
      self.plot_2.figure = anvil.server.call('get_shop_reviews', coffee_name)
      self.plot_3.figure = anvil.server.call('get_shop_sentiments', coffee_name)
      self.dashboard_data = anvil.server.call('get_dahsboard_data', coffee_name)
    else:
      self.drop_down_2.items =  ["2025", "2024", "2023", "2022", "2021", "2020", "2019","2018", "2017", "2016", "2015", "2014" ]
      self.drop_down_1.items = ["2025", "2024", "2023", "2022", "2021", "2020", "2019","2018", "2017", "2016", "2015", "2014" ]
      self.drop_down_2.items = self.first_coffee_shops
      self.label_3.text = "All Cofee Shops"
      self.drop_down_1.selected_value = str(general_year)
      self.drop_down_2.selected_value = top_shop
      self.plot_2.figure = anvil.server.call('get_total_review_counts',general_year, top_shop)
      self.plot_3.figure =anvil.server.call('get_reviews_chart')
      self.plot_1.figure = anvil.server.call('get_ratings_chart')
      self.dashboard_data = anvil.server.call('get_dahsboard_data')
    self.init_components(**properties)
    self.label_7.text = self.dashboard_data[0]
    self.label_9.text = self.dashboard_data[1]
    self.label_11.text = self.dashboard_data[2]
    self.label_15.text = self.dashboard_data[3]
    self.label_13.text = self.dashboard_data[4]


    # Any code you write here will run before the form opens.
