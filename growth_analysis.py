import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
import numpy as np
from styles import BRAND_COLORS, TITLE_STYLE, HEADER_WRAPPER

def calculate_growth_metrics(d1, d3):
    deals = d1.copy()
    calls = d3.copy()

    calls['call_start_time'] = pd.to_datetime(calls['call_start_time'], errors='coerce')
    calls['month_year'] = calls['call_start_time'].dt.to_period('M')

    monthly_staff = calls.groupby('month_year')['call_owner_name'].nunique().reset_index()
    monthly_staff.columns = ['month_year', 'active_staff']
    
    paid_deals = deals[deals['stage'].astype(str).str.strip().str.lower() == 'payment_done'].copy()
    
    cal_results = []
    for period in monthly_staff['month_year'].unique():
        active_names = calls[calls['month_year'] == period]['call_owner_name'].unique()
        revenue = paid_deals[paid_deals['deal_owner_name'].isin(active_names)]['initial_amount_paid'].sum()
        cal_results.append({
            'display_date': period.to_timestamp(),
            'active_staff': monthly_staff[monthly_staff['month_year'] == period]['active_staff'].values[0],
            'revenue': revenue
        })
    cal_data = pd.DataFrame(cal_results).sort_values('display_date')

    mgr_start = calls.groupby('call_owner_name')['call_start_time'].min().reset_index()
    mgr_start.columns = ['deal_owner_name', 'hire_date']
    
    df_staged = pd.merge(deals, mgr_start, on='deal_owner_name', how='inner')
    max_date = calls['call_start_time'].max()
    df_staged['tenure_months'] = (
        (max_date.year - df_staged['hire_date'].dt.year) * 12 +
        (max_date.month - df_staged['hire_date'].dt.month)
    ).clip(lower=0)

    curve_stats = df_staged.groupby('tenure_months').agg(
        total_leads=('id', 'count'),
        mgr_count=('deal_owner_name', 'nunique')
    ).reset_index()

    sales_cnt = df_staged[df_staged['stage'].astype(str).str.strip().str.lower() == 'payment_done'].groupby('tenure_months').size().reset_index(name='sales_cnt')
    curve_data = pd.merge(curve_stats, sales_cnt, on='tenure_months', how='left').fillna(0)
    curve_data['conv_rate'] = (curve_data['sales_cnt'] / curve_data['total_leads'] * 100).round(1)

    return cal_data, curve_data.sort_values('tenure_months')

def render_growth_tab(finalizer):
    try:
        cal_data, curve_data = calculate_growth_metrics(finalizer.d1, finalizer.d3)
    
        # --- FIGURE 1 ---
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=cal_data['display_date'], y=cal_data['active_staff'],
            name='Team Size', marker_color='#E5E5E5', opacity=0.35,
            text=cal_data['active_staff'], textposition='outside',
            yaxis='y2'
        ))
        fig1.add_trace(go.Scatter(
            x=cal_data['display_date'], y=cal_data['revenue'],
            name='Revenue', line=dict(color=BRAND_COLORS.get('sage', '#a4ac86'), width=4),
            mode='lines+markers'
        ))
        fig1.update_layout(
            title=None,
            yaxis=dict(title="Total Revenue ($)", side='left'),
            yaxis2=dict(title="Staff Count", overlaying='y', side='right', showgrid=False, range=[0, cal_data['active_staff'].max() * 1.3]),
            template="plotly_white",
            legend=dict(orientation="h", y=1.02, yanchor='bottom', x=0.5, xanchor='center'),
            margin=dict(t=30, l=40, r=40, b=40)
        )

        # --- FIGURE 2 ---
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=curve_data['tenure_months'], y=curve_data['total_leads'],
            name='Leads Processed', marker_color='#E5E5E5', opacity=0.35,
            text=curve_data['total_leads'], textposition='outside',
            yaxis='y2'
        ))
        fig2.add_trace(go.Scatter(
            x=curve_data['tenure_months'], y=curve_data['conv_rate'],
            name='Conversion Rate (%)', line=dict(color='#db9501', width=4),
            mode='lines+markers+text', 
            marker=dict(size=8, color='#db9501', line=dict(width=2, color='white')),
            text=curve_data['conv_rate'].apply(lambda x: f"{x}%"),
            textposition="top center",
            cliponaxis=False
        ))
        fig2.update_layout(
            title=None,
            xaxis=dict(title='Months of Experience (Tenure)', dtick=1),
            yaxis=dict(title='Conversion Rate (%)', side='left'),
            yaxis2=dict(title='Leads Volume', overlaying='y', side='right', showgrid=False, range=[0, max(1, curve_data['total_leads'].max() * 1.3)]),
            template='plotly_white',
            legend=dict(orientation='h', y=1.02, yanchor='bottom', x=0.5, xanchor='center'),
            margin=dict(t=30, l=40, r=40, b=40)
        )

        return html.Div([
            html.Div([
                html.H2("Scaling & Experience Analysis", style=TITLE_STYLE)
            ], style=HEADER_WRAPPER),
                
            # Chart 1 Title (Centered)
            html.Div("Team Size vs Revenue Correlation", 
                     style={'fontSize': '16px', 'fontWeight': 'bold', 'color': '#666', 'textAlign': 'center', 'marginTop': '10px'}),
            dcc.Graph(figure=fig1, config={'displayModeBar': False}),
           
            # Chart 2 Title (Centered)
            html.Div("Impact of Manager Tenure on Conversion Rate", 
                     style={'fontSize': '16px', 'fontWeight': 'bold', 'color': '#666', 'textAlign': 'center', 'marginTop': '20px'}),
            dcc.Graph(figure=fig2, config={'displayModeBar': False}),
                
            # Recommendation Box
            html.Div([
                html.B('Business Recommendation:'),
                html.P('Maintain an optimal headcount level to ensure efficient processing of all incoming leads. '
                       'As data shows, manager tenure directly impacts conversion efficiency, so focus on retention '
                       'to maximize ROI from marketing efforts.')
            ], style={
                'marginTop': '16px',
                'padding': '20px',
                'backgroundColor': '#f9f9f9',
                'borderLeft': f"5px solid {BRAND_COLORS.get('sage', '#a4ac86')}",
                'fontSize': '16px',
                'textAlign': 'left'
            })
        ], style={'padding': '0 16px'})
            
    except Exception as e:
        return html.Div(f"Critical Error: {e}", style={'color': 'red', 'padding': '20px'})