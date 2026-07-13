import plotly.graph_objects as go
from dash import html, dcc, dash_table
import pandas as pd
import numpy as np
from styles import BRAND_COLORS # Імпортуємо твої кольори

def render_campaign_tab(finalizer):
    paid_deals = finalizer.d1[finalizer.d1["stage"] == 'payment_done'].copy()
    df_revenue = paid_deals.groupby('source')['initial_amount_paid'].sum().reset_index(name="revenue")
    df_leads = finalizer.d1.groupby('source').size().reset_index(name='leads_count')

    d1_agg = pd.merge(df_leads, df_revenue, on='source', how='left').fillna(0)
    d2_agg = finalizer.d2.groupby('source').agg({'spend': 'sum', 'clicks': 'sum'}).reset_index()
    df = pd.merge(d1_agg, d2_agg, on='source', how='outer').fillna(0)

    df['CR%'] = np.where(df['clicks'] > 0, (df['leads_count'] / df['clicks'] * 100), 0).round(2)
    df['ROMI%'] = np.where(df['spend'] > 0, (df['revenue'] / df['spend'] * 100), 0).round(0)
    df['CAC'] = np.where(df['leads_count'] > 0, (df['spend'] / df['leads_count']), 0).round(2)
    df['CM'] = (df['revenue'] - df['spend']).round(0)

    df = df.sort_values(by='CM', ascending=False)
    df_plot = df[df['revenue'] > 0].copy()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_plot['source'],
        y=df_plot['ROMI%'],
        mode='markers+text',
        text=df_plot['source'],
        textposition='middle center',
        textfont=dict(size=9, color='black'),
        marker=dict(
            size=np.log1p(df_plot['leads_count']) * 25,
            color=df_plot['CM'],
            colorscale='Greens',
            showscale=False,
            line=dict(width=1, color='white')
        ),
        hovertemplate="<b>%{x}</b><br>ROMI: %{y}%<br>CAC: %{customdata[0]}<extra></extra>",
        customdata=df_plot[['CAC']]
    ))

    fig.update_layout(
        title={
            'text': "Marketing Sources: ROMI vs Contribution Margin",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 16, 'color': BRAND_COLORS['bark']}
        },
        height=560,
        margin=dict(l=40, r=40, t=80, b=40), # Збільшили 't', щоб назва влізла
        template="plotly_white",
        xaxis=dict(visible=False),
        yaxis=dict(title="ROMI %", tickfont=dict(size=10)),
        paper_bgcolor='rgba(0,0,0,0)',
        autosize=True
    )

    return html.Div([
        html.Div([
            html.H3("Campaign Performance and Unit Economics by Source", 
                    style={
                        'textAlign': 'left', 
                        'marginTop': '20px', 
                        'marginBottom': '20px',
                        'color': BRAND_COLORS['bark']
                    }),

            dcc.Graph(
                figure=fig,
                config={'displayModeBar': False},
                style={'height': '60vh', 'minHeight': '420px'}
            ),

            html.Div([
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{"name": i, "id": i} for i in df.columns],
                    style_table={'maxHeight': '30vh', 'overflowY': 'auto'},
                    style_cell={'textAlign': 'center', 'padding': '8px', 'fontSize': '11px', 'fontFamily': 'Arial'},
                    style_header={'fontWeight': 'bold', 'backgroundColor': '#f2f2f2', 'color': BRAND_COLORS['bark']},
                    style_data_conditional=[
                        {'if': {'column_id': 'ROMI%', 'filter_query': '{ROMI%} < 100 && {spend} > 0'}, 'backgroundColor': '#FFCCCC'},
                        {'if': {'column_id': 'ROMI%', 'filter_query': '{ROMI%} >= 100'}, 'backgroundColor': '#CCFFCC'}
                    ]
                )
            ], style={'marginTop': '20px'})

        ], style={'width': '100%', 'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 16px'})
    ], style={'height': '100%', 'display': 'flex', 'flexDirection': 'column'})