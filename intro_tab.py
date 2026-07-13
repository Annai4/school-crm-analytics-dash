from dash import html
from styles import BRAND_COLORS, TITLE_STYLE

def render_intro_tab():
    return html.Div([

        html.Div([
            html.H1("School X Operational Analytics",
                    style={'fontSize': '48px', 'color': BRAND_COLORS['bark'], 'marginBottom': '10px'}),

            html.H3("CRM data cleaning and analysis to improve school efficiency",
                    style={'fontSize': '24px', 'color': BRAND_COLORS['sage'], 'fontWeight': 'normal', 'marginBottom': '40px'}),

            html.Div(style={'height': '2px', 'backgroundColor': BRAND_COLORS['gold'], 'width': '100px', 'margin': '20px 0'}),

            html.P("Dataset: Jan–Dec 2024 • Scope: leads & deals from CRM • Tools: Python (Pandas, Plotly Dash) • Author: Hanna Ivanova (student Itcareerhub) • Date: Feb 2026",
                   style={'fontSize': '13px', 'color': '#777', 'marginTop': '20px'})

        ], style={'padding': '100px 40px', 'textAlign': 'left'})

    ], style={'height': '80vh', 'display': 'flex', 'alignItems': 'center'})