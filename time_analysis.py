import plotly.graph_objects as go
from dash import html, dcc
import pandas as pd
from styles import BRAND_COLORS

def render_time_tab(finalizer):
   
    df = finalizer.d1.copy()
    df['cycle_days'] = (df['closing_date'] - df['created_time']).dt.days
    df_closed = df[df['cycle_days'].notnull() & (df['cycle_days'] >= 0)].copy()

    deals_trend = df.resample('W', on='created_time').size().reset_index(name='deals_count')
    calls_trend = finalizer.d3.resample('W', on='call_start_time').size().reset_index(name='calls_count')
    cycle_trend = df_closed.resample('W', on='created_time')['cycle_days'].mean().reset_index(name='avg_cycle')

    trend_df = pd.merge(deals_trend, calls_trend, left_on='created_time', right_on='call_start_time', how='left')
    trend_df = pd.merge(trend_df, cycle_trend, on='created_time', how='left').fillna(0)


    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=trend_df['created_time'], y=trend_df['deals_count'],
        name="New Deals", mode='lines+markers', line=dict(color='#6e6702', width=3)
    ))

    fig.add_trace(go.Scatter(
        x=trend_df['created_time'], y=trend_df['calls_count'],
        name="Calling Activity", mode='lines', line=dict(color='#db9501', width=2, dash='dot'),
        yaxis="y2"
    ))

    fig.add_trace(go.Scatter(
        x=trend_df['created_time'], y=trend_df['avg_cycle'],
        name="Avg Cycle (Days)", mode='lines', line=dict(color='#4b4b4b', width=2),
        yaxis="y2"
    ))

    fig.update_layout(
        title={
            'text': "Time Series Analysis: Volume vs Activity vs Speed",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18, 'color': BRAND_COLORS['bark']}
        },
        xaxis=dict(title="Date"),
        yaxis=dict(title="Number of Deals", color='#6e6702'),
        yaxis2=dict(title="Calls / Days", overlaying="y", side="right", color='#db9501'),
        legend=dict(
            orientation='h', 
            x=0.5, 
            xanchor='center', 
            y=1.05, 
            yanchor='bottom', 
            title_text=''
        ),
        margin=dict(t=100, l=40, r=40, b=40), # Збільшений відступ зверху для центрування заголовка
        template="plotly_white",
        paper_bgcolor='rgba(0,0,0,0)',
        autosize=True
    )

    # --- Побудова Layout ---
    return html.Div([
        html.Div([
            # Заголовок сторінки ЗЛІВА (як ти і просила)
            html.H3("Temporal Trends and Operational Efficiency", 
                    style={'textAlign': 'left', 'marginTop': '20px', 'color': BRAND_COLORS['bark']}),
            
            # Графік з центрованою назвою всередині
            dcc.Graph(figure=fig, style={'height': '70vh', 'width': '100%'}),
            
            html.Div([
                html.P(
                    f"Current overall average sales cycle: {round(df_closed['cycle_days'].mean(), 1)} days.",
                    style={'fontWeight': 'bold', 'color': BRAND_COLORS['bark'], 'margin': 0}
                )
            ], style={'padding': '15px', 'backgroundColor': '#f2f2f2', 'borderRadius': '5px', 'marginTop': '10px'})
            
        ], style={'width': '100%', 'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 16px'})
    ])