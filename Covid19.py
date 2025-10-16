import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pycountry

# ============================================================
# Load and prepare data
# ============================================================

df = pd.read_csv("country_wise_latest.csv")

# Clean column names for consistency
df.columns = df.columns.str.strip()

# Add ISO-3 country codes for choropleth map
def country_to_iso3(name):
    try:
        return pycountry.countries.lookup(name).alpha_3
    except LookupError:
        return None

df["ISO3"] = df["Country/Region"].apply(country_to_iso3)

# ============================================================
# Initialize the Dash app
# ============================================================

app = dash.Dash(__name__)
app.title = "COVID-19 Global Dashboard"

# ============================================================
# App Layout
# ============================================================

app.layout = html.Div([
    html.H1("🌍 COVID-19 Global Trend Dashboard",
            style={'textAlign': 'center', 'color': '#1f77b4', 'marginTop': 20}),

    html.P("Interactive data visualization of the global COVID-19 situation.",
           style={'textAlign': 'center', 'color': '#444'}),

    # Dropdown for metric selection
    html.Div([
        html.Label("Select Metric:", style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='metric_dropdown',
            options=[
                {'label': 'Confirmed Cases', 'value': 'Confirmed'},
                {'label': 'Deaths', 'value': 'Deaths'},
                {'label': 'Recovered', 'value': 'Recovered'},
                {'label': 'Active Cases', 'value': 'Active'}
            ],
            value='Confirmed',
            clearable=False,
            style={'width': '60%'}
        )
    ], style={'textAlign': 'center', 'margin': '20px'}),

    # Summary cards
    html.Div([
        html.Div(id='total_confirmed', className='card'),
        html.Div(id='total_deaths', className='card'),
        html.Div(id='total_recovered', className='card'),
        html.Div(id='total_active', className='card'),
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '30px'}),

    # Choropleth map
    html.Div([
        dcc.Graph(id='world_map', style={'height': '600px'})
    ]),

    # Bar chart and scatter chart
    html.Div([
        html.Div([
            html.H3("Top 10 Countries", style={'textAlign': 'center'}),
            dcc.Graph(id='top10_bar')
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        html.Div([
            html.H3("Death vs Recovered Rate", style={'textAlign': 'center'}),
            dcc.Graph(id='scatter_plot')
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ], style={'marginTop': '30px', 'marginBottom': '50px'}),

    html.Footer("Created by Triston Marta — Data Science & Statistics Graduate",
                style={'textAlign': 'center', 'color': '#888', 'padding': '20px'})
])

# ============================================================
# Callbacks for interactivity
# ============================================================

@app.callback(
    [Output('world_map', 'figure'),
     Output('top10_bar', 'figure'),
     Output('scatter_plot', 'figure'),
     Output('total_confirmed', 'children'),
     Output('total_deaths', 'children'),
     Output('total_recovered', 'children'),
     Output('total_active', 'children')],
    [Input('metric_dropdown', 'value')]
)
def update_dashboard(selected_metric):
    # --------------------------
    # Map
    # --------------------------
    fig_map = px.choropleth(
        df,
        locations='ISO3',
        color=selected_metric,
        hover_name='Country/Region',
        color_continuous_scale='Reds' if selected_metric == 'Deaths' else 'Blues',
        title=f"Global {selected_metric} Cases",
        locationmode='ISO-3'
    )
    fig_map.update_layout(
        geo=dict(showframe=False, showcoastlines=False),
        margin=dict(l=0, r=0, t=50, b=0)
    )

    # --------------------------
    # Top 10 bar chart
    # --------------------------
    top10 = df.nlargest(10, selected_metric)
    fig_bar = px.bar(
        top10.sort_values(selected_metric, ascending=True),
        x=selected_metric,
        y='Country/Region',
        orientation='h',
        color='Country/Region',
        title=f"Top 10 Countries by {selected_metric}",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_bar.update_layout(showlegend=False)

    # --------------------------
    # Scatter plot
    # --------------------------
    fig_scatter = px.scatter(
        df,
        x='Recovered',
        y='Deaths',
        size='Confirmed',
        color='Active',
        hover_name='Country/Region',
        log_x=True,
        log_y=True,
        title="Recovered vs Deaths (Log Scale)"
    )

    # --------------------------
    # Summary cards
    # --------------------------
    total_confirmed = df['Confirmed'].sum()
    total_deaths = df['Deaths'].sum()
    total_recovered = df['Recovered'].sum()
    total_active = df['Active'].sum()

    confirmed_card = html.Div([
        html.H4("Confirmed", style={'color': '#007bff'}),
        html.H2(f"{total_confirmed:,}")
    ])
    deaths_card = html.Div([
        html.H4("Deaths", style={'color': '#dc3545'}),
        html.H2(f"{total_deaths:,}")
    ])
    recovered_card = html.Div([
        html.H4("Recovered", style={'color': '#28a745'}),
        html.H2(f"{total_recovered:,}")
    ])
    active_card = html.Div([
        html.H4("Active", style={'color': '#ffc107'}),
        html.H2(f"{total_active:,}")
    ])

    return fig_map, fig_bar, fig_scatter, confirmed_card, deaths_card, recovered_card, active_card


# ============================================================
# Run the App
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)
    Output('country-stats', 'children'),
    Output('bar-chart', 'figure'),
    Input('country-dropdown', 'value')

def update_country_data(selected_country):
    # Filter data for the selected country
    country_data = df[df['Country/Region'] == selected_country].iloc[0]

    confirmed = int(country_data['Confirmed'])
    deaths = int(country_data['Deaths'])
    recovered = int(country_data['Recovered'])
    active = int(country_data['Active'])

    stats_text = (
        f"📍 {selected_country} — Confirmed: {confirmed:,} | Deaths: {deaths:,} | "
        f"Recovered: {recovered:,} | Active: {active:,}"
    )

    # Bar chart for this country
    chart_df = pd.DataFrame({
        'Category': ['Confirmed', 'Deaths', 'Recovered', 'Active'],
        'Count': [confirmed, deaths, recovered, active]
    })

    fig = px.bar(chart_df, x='Category', y='Count', color='Category',
                 title=f"COVID-19 Cases Breakdown for {selected_country}",
                 text='Count')
    fig.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig.update_layout(template='plotly_white', title_x=0.5)

    return stats_text, fig


@app.callback(
    Output('world-map', 'figure'),
    Input('country-dropdown', 'value')
)
def update_map(_):
    fig = px.choropleth(
        df,
        locations="ISO3",
        locationmode="ISO-3",
        color="Confirmed",
        hover_name="Country/Region",
        hover_data=["Confirmed", "Deaths", "Recovered", "Active"],
        color_continuous_scale="Reds",
        title="Global COVID-19 Confirmed Cases"
    )
    fig.update_layout(geo=dict(showframe=False, showcoastlines=True),
                      template='plotly_white', title_x=0.5)
    return fig

# ---------------------------
# 5. Run App
# ---------------------------

if __name__ == '__main__':
    app.run(debug=True)