import anvil.files
from anvil.files import data_files
import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import plotly.graph_objects as go
import datetime
from collections import Counter
from operator import itemgetter
import time

@anvil.server.callable
def get_competitor_plot():
    a = time.time()
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
    top_clients = app_tables.shops.search(anvil.tables.order_by('reviews_count', ascending=False))

    current_year = datetime.datetime.now().year
    previous_year = current_year - 1
    
    monthly_counts = {}
    
    for year in [previous_year, current_year]:
        data = []
        for month in range(1, 13):
            start_date = datetime.datetime(year, month, 1)
            
            if month == 12:
                end_date = datetime.datetime(year, month, 31)
            else:
                end_date = datetime.datetime(year, month + 1, 1) - datetime.timedelta(days=1)
    
            reviews = app_tables.reviews.search(published_at=q.between(start_date, end_date), shop=q.any_of(*top_clients[:6]))
            
            data.append(len(reviews))
        monthly_counts[year] = data
    
    last_year = monthly_counts[current_year]
    this_year = monthly_counts[previous_year]

    last_year_trace = go.Scatter(
        x=months,
        y=last_year,
        mode='lines',
        name='Last year',
        line=dict(color='black', width=2)
    )

    this_year_trace = go.Scatter(
        x=months,
        y=this_year,
        mode='lines',
        name='This year',
        line=dict(color='lightblue', width=2, dash='dot')
    )

    fig = go.Figure(data=[last_year_trace, this_year_trace])

    fig.update_layout(
        title="Total reviews count over years",
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        legend=dict(
            orientation="h",
            x=0.02,
            y=1.15,
        ),
        plot_bgcolor="white"
    )
    return fig

@anvil.server.callable
def get_ratings_chart():
    client = app_tables.clients.search()[0]
    values = anvil.server.call('get_client_home_page', client)
    labels = [key for key, value in values]
    values = [value for key, value in values]
    colors = ["black", "lightblue", "lightgreen", "#d4e4fa"]

    # Create Donut Chart
    fig = go.Figure(
        data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            hole=0.5,
            textinfo="none",
        )]
    )

    fig.update_layout(
    title="Top Ratings",
    showlegend=True,
    legend=dict(
        orientation="v",
        x=1.1,
        y=1
    ),
    margin=dict(l=0, r=120, t=40, b=20),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

    return fig

@anvil.server.callable
def get_reviews_chart():
    c = time.time()
    top_clients = app_tables.shops.search(anvil.tables.order_by('reviews_count', ascending=False))
    categories = [client['shop_name'] for client in top_clients[:6]]
    values = [client['reviews_count'] for client in top_clients[:6]]
    colors = ["#A5A7FB", "#8EE2DA", "black", "#7DB9FF", "#AFC7E3", "#97E69A"]  # Custom colors
    fig = go.Figure(
        data=[go.Bar(
            x=categories,
            y=values,
            marker=dict(color=colors, line=dict(width=0)),
            width=0.3,
        )]
    )
    # Update Layout
    fig.update_layout(
        title="Total Reviews",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        plot_bgcolor="white",
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig

@anvil.server.callable
def get_user_cleint(user):
  return app_tables.clients.get(user=user)

@anvil.server.callable
def get_notifaicatons():
  return app_tables.notifications.search(tables.order_by('created_at', ascending=False))

@anvil.server.callable
def get_current_client():
  user = anvil.users.get_user()
  client = app_tables.clients.get(user=user)
  if client:
    return client
  return None


@anvil.server.callable
def get_home_page_rating(client=None):
    # Data
    b = time.time()
    if client:
      shop = app_tables.shops.get(shop_name=client)
    else:
      client = app_tables.clients.search()[0]
      shop = client['shop']
    
    bad_reviews = len(app_tables.reviews.search(shop=shop, label=0))
    satisfactory_reviews = len(app_tables.reviews.search(shop=shop, label=1))
    good_reviews = len(app_tables.reviews.search(shop=shop, label=2))
    labels = ["Unsatisfied", "Partially Satisfied" , "Satisfied"]
    values = [bad_reviews, good_reviews, satisfactory_reviews]
    colors = ["black", "lightblue", "lightgreen"]

    # Create Donut Chart
    fig = go.Figure(
        data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            hole=0.5,
            textinfo="none",
        )]
    )

    fig.update_layout(
    title="Customer satisfaction",
    showlegend=True,
    legend=dict(
        orientation="v",
        x=1.1,
        y=1
    ),
    margin=dict(l=0, r=120, t=40, b=20),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
    return fig

@anvil.server.callable
def enable_payment(user):
  payment = app_tables.subscription_types.search()[0]
  user['subscription_package'] = payment


@anvil.server.callable
def edit_profile(business_name, business_type, country, city, area):
  clinet = get_current_client()
  if clinet['business_name'] == business_name and clinet['business_type'] == business_type and clinet['country'] == country and clinet['city'] == city and clinet['area'] == area:
    return False
  if clinet['business_name'] != business_name:
    shop = app_tables.shops.get(shop_name=business_name)
    if shop:
      clinet['shop'] = shop
    else:
      clinet['shop'] = None
  clinet['business_name'] = business_name
  clinet['business_type'] = business_type
  clinet['country'] = country
  clinet['city'] = city
  clinet['area'] = area
  return True

@anvil.server.callable
def delete_user_account():
  user = anvil.users.get_user()
  user['deleted_at'] = datetime.datetime.now()

@anvil.server.callable
def reactivate_deleted_account():
  user = anvil.users.get_user()
  user['deleted_at'] = None


@anvil.server.callable
def send_approval_email(email, approved):
  print("here in funcx")
  print("email: ", email)
  if approved:
    print("in if")
    anvil.email.send(to=email, subject="Approved by business Trend Admin",text=f"""
    You are approved! Please enter to complete the payment to
activate your account {anvil.server.get_app_origin('published')}
  Thanks!
  """ )
  else:
    print("in else")
    anvil.email.send(to=email, subject="Rejecteed by business Trend Admin",text="""We’re sorry to inform you that you have been rejected. Please
  contact us for further information Seniorprojectbtsa@gmail.com
  Thanks!
  """ )