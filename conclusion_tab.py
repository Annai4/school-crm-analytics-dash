from dash import html
from styles import BRAND_COLORS

def render_conclusion_tab():
    return html.Div([
        html.H2("Conclusions & Strategic Recommendations",
                style={'textAlign': 'left', 'color': BRAND_COLORS['bark'], 'marginBottom': '30px'}),

        html.Div([
            html.H4("CRM Data Integrity", style={'color': BRAND_COLORS['forest'], 'margin': '0 0 10px 0'}),
            html.P("Implement strict CRM guidelines: replace manual text entry with dropdown selection to prevent data duplication and ensure accurate reporting.",
                   style={'margin': 0})
        ], style={'padding': '20px', 'backgroundColor': '#f9f9f9', 'borderLeft': f"5px solid {BRAND_COLORS['gold']}", 'marginBottom': '20px'}),

        html.H3("Next actions", style={'marginTop': '40px', 'color': BRAND_COLORS['bark']}),

        html.Ul([
            html.Li("Rebalance lead distribution across tiers to maximize high-performer ROI", style={'marginBottom': '10px'}),
            html.Li("Invest in onboarding playbooks and retention to build a senior sales core", style={'marginBottom': '10px'}),
            html.Li("Monitor monthly: track 'team size vs revenue' and 'tenure vs conversion' as key KPIs", style={'marginBottom': '10px'}),
            html.Li("A/B-test delay/threshold rules in CRM for automated lead reassignment", style={'marginBottom': '10px'}),
        ], style={'fontSize': '18px', 'lineHeight': '1.8'}),

        html.Div([
            html.H3("Thank you for your attention!", style={'color': BRAND_COLORS['bark']}),
            html.P("Ready for Q&A session regarding operational optimization.", style={'color': '#666'})
        ], style={'marginTop': '60px', 'borderTop': '1px solid #eee', 'paddingTop': '30px', 'textAlign': 'center'})

    ], style={'padding': '40px 16px', 'maxWidth': '1000px', 'margin': '0 auto'})