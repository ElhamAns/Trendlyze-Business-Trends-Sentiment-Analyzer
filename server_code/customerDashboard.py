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
def get_total_review_counts(year=2025):
    a = time.time()
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
    top_clients = app_tables.shops.search(anvil.tables.order_by('reviews_count', ascending=False))

    year = int(year)
    monthly_counts = {}
    for clinet in top_clients[:6]:
        data = []
        for month in range(1, 13):
            start_date = datetime.datetime(year, month, 1)
            if month == 12:
                end_date = datetime.datetime(year, month, 31)
            else:
                end_date = datetime.datetime(year, month + 1, 1) - datetime.timedelta(days=1)
            reviews = app_tables.reviews.search(published_at=q.between(start_date, end_date), shop=clinet)
            data.append(len(reviews))
        monthly_counts[clinet['shop_name']] = data

    line_data = {}
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown'] 
    for i, client in enumerate(top_clients[:6]):
        shop_name = client['shop_name']
        color_index = i % len(colors)
        line_data[shop_name] = {
            'data': monthly_counts[shop_name],
            'color': colors[color_index],
            'width': 2,
            'dash': None
        }


    traces = []
    for name, config in line_data.items():
        trace = go.Scatter(
            x=months,
            y=config['data'],
            mode='lines',
            name=name,
            line=dict(color=config['color'], width=config['width'], dash=config['dash'])
        )
        traces.append(trace)
    fig = go.Figure(data=traces)
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
def get_shop_reviews(shop_name):
    a = time.time()
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
    shop = app_tables.shops.get(shop_name=shop_name)

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
            reviews = app_tables.reviews.search(published_at=q.between(start_date, end_date), shop=shop)
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
    print("time taken a: ", time.time() - a)
    return fig

@anvil.server.callable
def get_shop_sentiments(shop_name=None):
    c = time.time()
    shop = app_tables.shops.get(shop_name=shop_name)
    group_labels = ["Satisfied", "Satisfied", "Partially Satisfied", "Partially Satisfied", "Unsatisfied", "Unsatisfied"]
    categories = ["Real Sentiment", "Rating on Google Maps", "Real Sentiment","Rating on Google Maps", "Real Sentiment", "Rating on Google Maps"]
    satisfied_sentiment = len(app_tables.reviews.search(label=2, shop=shop))
    partially_satisfied_sentiment = len(app_tables.reviews.search(label=1, shop=shop))
    un_satisfied_sentiment = len(app_tables.reviews.search(label=0, shop=shop))

    satisfied_rating = len(app_tables.reviews.search(stars=q.any_of(*[4,5]), shop=shop))
    partially_satisfied_rating = len(app_tables.reviews.search(stars=3, shop=shop))
    un_satisfied_rating = len(app_tables.reviews.search(stars=q.any_of(*[2,1]), shop=shop))
  
    values = [satisfied_sentiment, satisfied_rating, partially_satisfied_sentiment, partially_satisfied_rating, un_satisfied_sentiment, un_satisfied_rating]
    colors = ["#A5A7FB", "#8EE2DA", "black", "#7DB9FF", "#AFC7E3", "#97E69A"]
    fig = go.Figure()
    for i in range(6):
        fig.add_trace(go.Bar(
            x=[group_labels[i]],
            y=[values[i]],
            name=categories[i],
            marker=dict(color=colors[i]),
            width=0.3,
            text=categories[i],
            hoverinfo="text+y"
        ))
    # fig = go.Figure(
    #     data=[go.Bar(
    #         x=categories,
    #         y=values,
    #         marker=dict(color=colors, line=dict(width=0)),
    #         width=0.3,  # Adjust bar width
    #     )]
    # )
    # Update Layout
    fig.update_layout(
        title="Total Reviews",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        plot_bgcolor="white",
        barmode='group',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    print("time taken c: ", time.time() - c)

    return fig