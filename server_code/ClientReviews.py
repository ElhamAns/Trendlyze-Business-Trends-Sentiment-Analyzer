import anvil.files
from anvil.files import data_files
import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def get_client_reviews(shop_name, rating_filter=None):
  shop = app_tables.shops.get(shop_name=shop_name)
  if not rating_filter or rating_filter=="All Reviews":
    reviews = app_tables.reviews.search(shop=shop)
    return reviews
  if rating_filter=="Satisfied":
    reviews = app_tables.reviews.search(shop=shop, label=2)
    return reviews
  if rating_filter=="Partially Satisfied":
    reviews = app_tables.reviews.search(shop=shop, label=1)
    return reviews
  if rating_filter=="Dissatisfied":
    reviews = app_tables.reviews.search(shop=shop, label=0)
    return reviews

@anvil.server.callable
def get_client_review_type(shop_name, rating_filter, review_type):
    shop = app_tables.shops.get(shop_name=shop_name)
    if not shop:
        return []

    label_map = {
        "Satisfied": 2,
        "Partially Satisfied": 1,
        "Dissatisfied": 0
    }

    search_kwargs = {"shop": shop}

    if rating_filter and rating_filter != "All Review":
        label_value = label_map.get(rating_filter)
        if label_value is not None:
            search_kwargs["label"] = label_value

    if not review_type or review_type == "All Reviews":
        return app_tables.reviews.search(**search_kwargs)

    review_type_field = review_type.lower()
    search_kwargs[review_type_field] = True
    return app_tables.reviews.search(**search_kwargs)
