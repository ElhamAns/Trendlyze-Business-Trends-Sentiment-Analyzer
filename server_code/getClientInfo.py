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
    
    # Initialize a dictionary to store the count of reviews per month
    monthly_counts = {}
    
    # Loop through each year (current year and previous year)
    for year in [previous_year, current_year]:
        data = []
        # Loop through each month (1 to 12)
        for month in range(1, 13):
            # Create the start and end date for the month
            start_date = datetime.datetime(year, month, 1)
            
            # For months other than December, set the end date to the last day of the month
            if month == 12:
                end_date = datetime.datetime(year, month, 31)
            else:
                # For months with 31 days
                end_date = datetime.datetime(year, month + 1, 1) - datetime.timedelta(days=1)
    
            # Query the reviews table for reviews published within this month
            reviews = app_tables.reviews.search(published_at=q.between(start_date, end_date), shop=q.any_of(*top_clients[:6]))
            
            # Store the count of reviews for this month in the dictionary
            data.append(len(reviews))
        monthly_counts[year] = data
    
    last_year = monthly_counts[current_year]
    this_year = monthly_counts[previous_year]

    # Create traces as separate Scatter objects
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

    # Create Figure and pass traces in the `data` argument
    fig = go.Figure(data=[last_year_trace, this_year_trace])

    # Update Layout
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
    print("time taken a: ", time.time() - a)
    return fig

@anvil.server.callable
def get_ratings_chart():
    # Data
    b = time.time()
    user = app_tables.users.get(email="me.mansoor006@gmail.com")
    client = app_tables.clients.search()[0]
    values = anvil.server.call('get_client_home_page', client)
    labels = [key for key, value in values]
    values = [value for key, value in values]
    colors = ["black", "lightblue", "lightgreen", "#d4e4fa"]  # Custom colors

    # Create Donut Chart
    fig = go.Figure(
        data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            hole=0.5,  # Donut effect
            textinfo="none",  # Hide percentage labels on the chart
        )]
    )

    # Update Layout
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

    print("time taken b: ", time.time() - b)
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
            width=0.3,  # Adjust bar width
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
    print("time taken c: ", time.time() - c)

    return fig

@anvil.server.callable
def get_user_cleint(user):
  return app_tables.clients.get(user=user)

@anvil.server.callable
def get_notifaicatons():
  return app_tables.notifications.search(tables.order_by('created_at'))

@anvil.server.callable
def get_current_client():
  user = app_tables.users.get(email="me.mansoor006@gmail.com")
  # user = anvil.users.get_user()
  client = app_tables.clients.get(user=user)
  return client


@anvil.server.callable
def get_home_page_rating(client=None):
    # Data
    b = time.time()
    if client:
      shop = app_tables.shops.search(shop_name=client)[0]
    else:
      user = app_tables.users.get(email="me.mansoor006@gmail.com")
      client = app_tables.clients.search()[0]
      shop = client['shop']
    
    bad_reviews = len(app_tables.reviews.search(shop=shop, label=0))
    satisfactory_reviews = len(app_tables.reviews.search(shop=shop, label=1))
    good_reviews = len(app_tables.reviews.search(shop=shop, label=2))
    print("time taken before: ", time.time() - b)
    
    labels = ["Unsatisfied", "Partially Satisfied" , "Satisfied"]
    values = [bad_reviews, good_reviews, satisfactory_reviews]
    colors = ["black", "lightblue", "lightgreen"]  # Custom colors

    # Create Donut Chart
    fig = go.Figure(
        data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            hole=0.5,  # Donut effect
            textinfo="none",  # Hide percentage labels on the chart
        )]
    )

    # Update Layout
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

    print("time taken b: ", time.time() - b)
    return fig