import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import plotly.graph_objects as go

@anvil.server.callable
def get_competitor_plot():
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]
    last_year = [9000, 7000, 12000, 18000, 25000, 21000, 23000]
    this_year = [10000, 14000, 9000, 16000, 22000, 24000, 26000]

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
        title="Total Competitors in Market",
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
    # Data
    labels = ["Andes", "Hassad", "Rateel", "Saje"]
    values = [52.1, 22.8, 13.9, 11.2]  # Percentages
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


    return fig

@anvil.server.callable
def get_reviews_chart():
    # Data
    categories = ["OWL", "Rateel", "Andes", "Hassad", "Saje", "Line"]
    values = [15000, 30000, 20000, 32000, 12000, 22000]  # Number of reviews
    colors = ["#A5A7FB", "#8EE2DA", "black", "#7DB9FF", "#AFC7E3", "#97E69A"]  # Custom colors

    # Create Bar Chart
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

    return fig

@anvil.server.callable
def get_user_cleint(user):
  return app_tables.clients.get(user=user)

@anvil.server.callable
def get_notifaicatons():
  return app_tables.notifications.search(tables.order_by('created_at'))

@anvil.server.callable
def get_current_client():
  user = anvil.users.get_user()
  client = app_tables.clients.get(user=user)
  return client

@anvil.server.callable
def get_client_compitetors():
  return [
    {"No": 1, "Competitor": "OWL", "Contact Information": "+966 50 441 5467", "Location": "Khobar, King Khaled St."},
    {"No": 2, "Competitor": "ANDES", "Contact Information": "+966 54 460 7313", "Location": "Khobar, Prince Talal St."},
    {"No": 3, "Competitor": "LINE", "Contact Information": "+966 51 061 5946", "Location": "Khobar, 21st St."},
    {"No": 4, "Competitor": "RATEEL", "Contact Information": "+966 56 434 2883", "Location": "Khobar, Prince Naif St."},
    {"No": 5, "Competitor": "SAJE", "Contact Information": "+966 54 070 7691", "Location": "Khobar, 13th St."}
]
