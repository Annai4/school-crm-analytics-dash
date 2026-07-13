import pandas as pd
import plotly.express as px
from dash import dcc, html
from styles import BRAND_COLORS 

def render_performance_tab(finalizer):
    try:
        paid_deals = finalizer.d1[finalizer.d1['stage'] == 'payment_done'].copy()
        successful_contact_ids = paid_deals['contact_name'].unique()

        top_list = paid_deals.groupby('deal_owner_name').size().nlargest(10).index.tolist()
        all_with_sales = paid_deals['deal_owner_name'].unique()

        def get_tier(name):
            if name in top_list: return 'Top Performer'
            if name in all_with_sales: return 'Middle'
            return 'Outsider'

        relevant_calls = finalizer.d3[
            (finalizer.d3['contactid'].isin(successful_contact_ids)) & 
            (finalizer.d3['call_duration_in_min'] > 0)
        ]
        
        effort_df = pd.DataFrame({
            'calls': relevant_calls.groupby('call_owner_name').size(),
            'deals': paid_deals.groupby('deal_owner_name').size()
        }).fillna(0)

        effort_df = effort_df[effort_df['deals'] > 0].reset_index().rename(columns={'index': 'manager'})
        effort_df['tier'] = effort_df['manager'].apply(get_tier)
        effort_df['calls_per_deal'] = (effort_df['calls'] / effort_df['deals']).round(1)

        df_v = finalizer.d3[finalizer.d3['call_duration_in_min'] > 0].copy()
        df_v['call_duration_in_min'] = df_v['call_duration_in_min'].round(1)
        df_v['tier'] = df_v['call_owner_name'].apply(get_tier)

        fig_violin = px.violin(
            df_v, y="call_duration_in_min", x="tier", color="tier", 
            box=True, points="outliers",
            color_discrete_map={'Top Performer': BRAND_COLORS['gold'], 'Middle': BRAND_COLORS['forest'], 'Outsider': '#999999'}
        )

        fig_box = px.box(
            effort_df, x="tier", y="calls_per_deal", color="tier", points="all",
            color_discrete_map={'Top Performer': BRAND_COLORS['bronze'], 'Middle': BRAND_COLORS['algae'], 'Outsider': '#999999'}
        )

        fig_violin.update_traces(hovertemplate="<b>%{x}</b><br>Median: %{median:.1f} min<extra></extra>")
        
        fig_box.update_traces(selector=dict(type='box'), hovertemplate="<b>Group: %{x}</b><br>Median: %{median:.1f}<extra></extra>")
        fig_box.update_traces(selector=dict(mode='markers'), customdata=effort_df[['manager']], 
                              hovertemplate="<b>%{customdata[0]}</b><br>Calls/Deal: %{y:.1f}<extra></extra>")

        fig_violin.update_layout(title={'text': "<b>Talk Time Distribution</b>", 'x': 0.5, 'xanchor': 'center'})
        fig_box.update_layout(title={'text': "<b>Efficiency: Calls per Deal</b>", 'x': 0.5, 'xanchor': 'center'})

        for fig in (fig_violin, fig_box):
            fig.update_layout(
                template='plotly_white', 
                showlegend=False, 
                margin=dict(t=60, b=40, l=40, r=40)
            )
            fig.update_xaxes(
                categoryorder='array', 
                categoryarray=['Top Performer', 'Middle', 'Outsider'],
                title=""
            )

        return html.Div([
            html.H3('Performance Deep Dive: Manager Efficiency Distribution',
                    style={'textAlign': 'left', 'margin': '10px 0 16px 0', 'color': BRAND_COLORS['bark'], 'fontWeight': 600}),
            
            html.Div([
                dcc.Graph(figure=fig_violin, config={'displayModeBar': False}, style={'height': '60vh', 'width': '100%', 'margin': 0, 'padding': 0}),
                dcc.Graph(figure=fig_box,    config={'displayModeBar': False}, style={'height': '60vh', 'width': '100%', 'margin': 0,
                                                                                      'padding': 0})],
                style={'padding': '0 16px 8px', 'margin': 0}),

            html.Div([
                html.B('How to read these charts:', style={'color': BRAND_COLORS['bark']}),
                html.P('On the left, we see the talk time distribution (min). On the right — the number of '
                       'calls required to close a single deal. Each dot represents an individual manager.')
            ], style={'padding': '0 16px 8px', 'margin': 0})
        ])

    except Exception as e:
        return html.Div(f"Error loading tab: {str(e)}", style={'color': 'red', 'padding': '20px'})