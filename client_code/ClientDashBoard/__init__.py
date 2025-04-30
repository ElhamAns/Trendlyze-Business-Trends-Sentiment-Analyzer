from ._anvil_designer import ClientDashBoardTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Reviews import Reviews


class ClientDashBoard(ClientDashBoardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.current_client = anvil.server.call('get_current_client')
    self.first_coffee_shops = anvil.server.call('get_all_coffee_shop', True)
    self.first_coffee_shops.append("All Coffee Shops") 
    self.dashboard_data = anvil.server.call('get_dahsboard_data')
    self.init_components(**properties)
    self.label_4.text = self.current_client['business_name']
    self.image_3.source = self.current_client['logo']
    self.label_7.text = self.dashboard_data[0]
    self.label_9.text = self.dashboard_data[1]
    self.label_11.text = self.dashboard_data[2]
    self.label_15.text = self.dashboard_data[3]
    self.label_13.text = self.dashboard_data[4]
    self.drop_down_1.items = ["2025", "2024", "2023", "2022", "2021", "2020", "2019","2018", "2017", "2016", "2015", "2014" ]
    self.drop_down_1.selected_value = "2024"
    self.drop_down_2.items = self.first_coffee_shops
    self.plot_1.figure = anvil.server.call('get_ratings_chart')
    self.drop_down_3.items = anvil.server.call('get_all_coffee_shop')
    self.plot_2.figure = anvil.server.call('get_total_review_counts',2024, self.first_coffee_shops[0])
    self.plot_3.figure = anvil.server.call('get_reviews_chart')


  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    response = alert("Are you sure you want to Logout?", buttons=["Yes", "No"])
    if response == "Yes":
      anvil.server.call('get_session_unauthenticated')
      anvil.users.logout()
      alert("Users logged out successfully")
      open_form('Form1')

  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ClientHomePage')
    
  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ClientSettings')

  def drop_down_3_change(self, **event_args):
    if not self.drop_down_3.selected_value:
          self.first_coffee_shops = anvil.server.call('get_all_coffee_shop', True)
          self.first_coffee_shops.append("All Coffee Shops") 
          self.dashboard_data = anvil.server.call('get_dahsboard_data')
          self.label_7.text = self.dashboard_data[0]
          self.label_9.text = self.dashboard_data[1]
          self.label_11.text = self.dashboard_data[2]
          self.label_15.text = self.dashboard_data[3]
          self.label_13.text = self.dashboard_data[4]
          self.drop_down_1.items = ["2025", "2024", "2023", "2022", "2021", "2020", "2019","2018", "2017", "2016", "2015", "2014" ]
          self.drop_down_1.selected_value = "2024"
          self.drop_down_2.items = self.first_coffee_shops
          self.plot_1.figure = anvil.server.call('get_ratings_chart')
          self.drop_down_3.items = anvil.server.call('get_all_coffee_shop')
          self.plot_2.figure = anvil.server.call('get_total_review_counts',2024, self.first_coffee_shops[0])
          self.plot_3.figure = anvil.server.call('get_reviews_chart')
          self.label_1.text = "Total Reviews count over a year"
          self.button_6.visible = False
    else:
        """This method is called when an item is selected"""
        self.dashboard_data = anvil.server.call('get_dahsboard_data', self.drop_down_3.selected_value)
        self.label_1.text = "Total Reviews count over years"
        self.label_7.text = self.dashboard_data[0]
        self.label_9.text = self.dashboard_data[1]
        self.label_11.text = self.dashboard_data[2]
        self.label_15.text = self.dashboard_data[3]
        self.label_13.text = self.dashboard_data[4]
        self.label_2.text = "Real Customer Sentiments"
        self.drop_down_1.items =  ["2025", "2024", "2023", "2022", "2021", "2020", "2019","2018", "2017", "2016", "2015", "2014" ]
        self.drop_down_1.selected_value = "2024"
        self.drop_down_2.selected_value = "2025"
        self.drop_down_2.items =  ["2025", "2024", "2023", "2022", "2021", "2020", "2019","2018", "2017", "2016", "2015", "2014" ]
        self.plot_1.figure = anvil.server.call('get_home_page_rating', self.drop_down_3.selected_value)
        self.plot_2.figure = anvil.server.call('get_shop_reviews', self.drop_down_3.selected_value)
        self.plot_3.figure = anvil.server.call('get_shop_sentiments', self.drop_down_3.selected_value)
        self.button_6.visible = True

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    if self.drop_down_3.selected_value==None:
        self.plot_2.figure = anvil.server.call('get_total_review_counts', year = self.drop_down_1.selected_value, shop=self.first_coffee_shops[0])
        self.drop_down_2.selected_value = self.first_coffee_shops[0]

  def drop_down_2_change(self, **event_args):
    """This method is called when an item is selected"""
    if not self.drop_down_3.selected_value:
        if self.drop_down_2.selected_value == "All Coffee Shops":
            self.plot_2.figure = anvil.server.call('get_total_review_counts', self.drop_down_1.selected_value)
        else:
            self.plot_2.figure = anvil.server.call('get_total_review_counts', self.drop_down_1.selected_value, shop=self.drop_down_2.selected_value)
    else:
        self.plot_2.figure = anvil.server.call('get_shop_reviews', shop_name=self.first_coffee_shops[0], start_year=self.drop_down_1.selected_value, end_year=self.drop_down_2.selected_value)
      
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    media_object = anvil.server.call('create_zaphod_pdf', self.drop_down_3.selected_value,general_year=self.drop_down_1.selected_value, top_shop_name=self.drop_down_2.selected_value, start_year = self.drop_down_1.selected_value, end_year= self.drop_down_2.selected_value)
    anvil.media.download(media_object)
    
  def view_review_button_visible(self):
    if not self.drop_down_3.selected_value:
      return False
    return True

  def button_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.open_form(Reviews(item=self.drop_down_3.selected_value))

  def policy_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ServicePage')

  def privacy_statement_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('PrivacyPolicy')
    
