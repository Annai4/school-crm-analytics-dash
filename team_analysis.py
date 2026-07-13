import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc
import pandas as pd
from styles import BRAND_COLORS

GENDER_MAP = {
    'Rachel White': 'female', 'Charlie Davis': 'male', 'Bob Brown': 'male',
    'Nina Scott': 'female', 'Alice Johnson': 'female', 'Ian Miller': 'male',
    'Jane Smith': 'female', 'Julia Nelson': 'female', 'George King': 'male',
    'Quincy Vincent': 'male', 'Diana Evans': 'female', 'Kevin Parker': 'male',
    'Ulysses Adams': 'male', 'Victor Barnes': 'male', 'Yara Edwards': 'female',
    'Paula Underwood': 'female', 'Mason Roberts': 'male', 'Ben Hall': 'male',
    'Amy Green': 'female', 'Cara Iverson': 'female', 'Oliver Taylor': 'male',
    'Eva Kent': 'female', 'Zachary Foster': 'male', 'Sam Young': 'male',
    'Wendy Clark': 'female', 'Tina Zhang': 'female', 'Derek James': 'male'
}

def render_team_tab(finalizer):
    df = finalizer.d1.copy()

    df['deal_owner_name'] = df['deal_owner_name'].astype(str).str.replace('_', ' ').str.title().str.strip()
    df['gender'] = df['deal_owner_name'].map(GENDER_MAP)
    df_clean = df.dropna(subset=['gender']).copy()
    df_clean['is_sale'] = df_clean['stage'].str.strip().str.lower().eq('payment_done')

    mgr_stats = df_clean.groupby('deal_owner_name').agg(
        leads=('id', 'count'),
        sales=('is_sale', 'sum')
    ).reset_index().sort_values('sales', ascending=False)

    top_10_names = mgr_stats.head(10)['deal_owner_name'].tolist()
    outsiders_names = mgr_stats[mgr_stats['sales'] == 0]['deal_owner_name'].tolist()

    def get_group(name):
        if name in top_10_names: return 'Top-10 Stars'
        if name in outsiders_names: return 'Outsiders (0 Sales)'
        return 'Middle Tier'

    mgr_stats['group'] = mgr_stats['deal_owner_name'].apply(get_group)
    group_data = mgr_stats.groupby('group')['leads'].sum().reset_index()
    total_leads = group_data['leads'].sum()

    leads_map = pd.Series(group_data.leads.values / total_leads, index=group_data.group).to_dict()

    team_gender = df_clean.groupby('gender')['deal_owner_name'].nunique().reset_index()
    team_gender.columns = ['gender', 'count']
    
    fig_donut = px.pie(
        team_gender, names='gender', values='count', 
        hole=0.55,
        color='gender', 
        color_discrete_map={
            'female': BRAND_COLORS.get('gold', '#C38E3D'),
            'male': BRAND_COLORS.get('forest', '#587B4C')
        }
    )
    fig_donut.update_traces(textinfo='percent', textposition='inside', textfont_size=14)
    fig_donut.update_layout(
        title=None,
        legend=dict(orientation='h', x=0.5, xanchor='center', y=1.02, yanchor='bottom', title_text=''),
        margin=dict(t=36, l=40, r=40, b=40), 
        template='plotly_white'
    )

    categories = ['Top-10 Stars', 'Middle Tier', 'Outsiders (0 Sales)']
    r_values = [leads_map.get(cat, 0) for cat in categories]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=r_values,
        theta=categories,
        fill='toself',
        name='Leads Share %',
        line=dict(color=BRAND_COLORS.get('bark', '#2e2300'), width=2),
        fillcolor='rgba(46, 35, 0, 0.2)'
    ))

    fig_radar.update_layout(
        title=None,
        polar=dict(
            radialaxis=dict(
                visible=True, 
                tickformat='.0%', 
                tickfont=dict(size=11),
                gridcolor="#eee"
            ),
            angularaxis=dict(gridcolor="#eee")
        ),
        legend=dict(orientation='h', x=0.5, xanchor='center', y=1.02, yanchor='bottom', title_text=''),
        margin=dict(t=36, l=40, r=40, b=40), 
        template='plotly_white'
    )

    return html.Div([
        html.H3('Team Composition & Resource Allocation', 
                style={'textAlign': 'left', 'margin': '8px 0 12px 0', 'color': BRAND_COLORS.get('bark', '#2e2300')}),

        html.Div([
            dcc.Graph(figure=fig_donut, style={'height': '60vh', 'width': '100%'}, config={'displayModeBar': False}),
            dcc.Graph(figure=fig_radar, style={'height': '60vh', 'width': '100%'}, config={'displayModeBar': False})
        ], style={
            'display': 'grid', 
            'gridTemplateColumns': 'repeat(2, 1fr)', 
            'gap': '24px', 
            'alignItems': 'stretch',
            'marginBottom': '24px'
        }),

        html.Div([
            html.H4("Strategic Insight:", style={'margin': '0 0 10px 0', 'color': BRAND_COLORS.get('crimson', '#800000')}),
            html.P(
                f"The 'Outsiders' group currently handles {leads_map.get('Outsiders (0 Sales)', 0)*100:.1f}% "
                "of the total lead volume. Reallocating these resources to 'Top-10 Stars' or the 'Middle Tier' "
                "could significantly improve overall conversion rates.",
                style={'margin': 0}
            )
        ], style={
            'padding': '20px',
            'backgroundColor': '#f9f9f9',
            'borderRadius': '8px',
            'borderLeft': f"6px solid {BRAND_COLORS.get('crimson', '#800000')}",
            'textAlign': 'left'
        })

    ], style={'padding': '0 16px'})