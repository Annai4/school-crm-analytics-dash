import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, callback, State, ctx
from finalizernew import DataFinalizer
from data_hygiene import render_hygiene_tab
from descriptive_stats import render_stats_tab
#from data_utils import apply_standardization
from time_analysis import render_time_tab
from campaign_analysis import render_campaign_tab
from team_analysis import render_team_tab
from performance_analysis import render_performance_tab
from growth_analysis import render_growth_tab
from unit_economics import render_unit_tab
from styles import BRAND_COLORS, TABS_STYLES, TAB_STYLE, TAB_SELECTED_STYLE
from intro_tab import render_intro_tab
from conclusion_tab import render_conclusion_tab


d1_clean = pd.read_excel('Deals_1Clean.xlsx')
d2_clean = pd.read_excel('Spend_1Clean.xlsx')
d3_clean = pd.read_excel('Calls_Cleaned.xlsx')
d4_clean = pd.read_excel('Contacts_Cleaned.xlsx')

d1_raw = pd.read_excel('Deals (Done).xlsx')
d2_raw = pd.read_excel('Spend (Done).xlsx')
d3_raw = pd.read_excel('Calls (Done).xlsx')
d4_raw = pd.read_excel('Contacts (Done).xlsx')


raw_tables = {'d1': d1_raw, 'd2': d2_raw, 'd3': d3_raw, 'd4': d4_raw}
clean_tables = {'d1': d1_clean, 'd2': d2_clean, 'd3': d3_clean, 'd4': d4_clean}

finalizer = DataFinalizer(raw_tables, clean_tables)
finalizer_clean = DataFinalizer(clean_tables, clean_tables)

raw_data_counts = {'Deals': len(d1_raw), 'Contacts': len(d4_raw)}

app = Dash(__name__)

app.layout = html.Div([  
    html.Div([
        html.Button('❮', id='tabs-prev', n_clicks=0, 
                    style={'height': '45px', 'backgroundColor': '#eee', 'border': '1px solid #ccc', 'cursor': 'pointer'}),
        
        html.Div([
            dcc.Tabs(
                id="tabs-nav", 
                value='tab-1', 
                style=TABS_STYLES, 
                children=[
                    dcc.Tab(label='Intro', value='tab-1', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                    dcc.Tab(label='Data Hygiene', value='tab-2', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                    dcc.Tab(label='Descriptive Stats', value='tab-3', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                    dcc.Tab(label='Time Dynamics', value='tab-4', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                    dcc.Tab(label='Campaign Analysis', value='tab-5', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                    dcc.Tab(label='Unit Economics', value='tab-6', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                    dcc.Tab(label='Performance Analysis', value='tab-7', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                    dcc.Tab(label='Growth & Experience', value='tab-8', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                    dcc.Tab(label='Team Analysis', value='tab-9', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                    dcc.Tab(label='Conclusion', value='tab-10', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                ]
            )
        ], style={'overflowX': 'hidden', 'flex': '1'}), 
        
        html.Button('❯', id='tabs-next', n_clicks=0, 
                    style={'height': '45px', 'backgroundColor': '#eee', 'border': '1px solid #ccc', 'cursor': 'pointer'}),
                    
    ], style={'display': 'flex', 'alignItems': 'center', 'gap': '5px', 'backgroundColor': '#f9f9f9', 'padding': '5px'}),

    html.Div(id='tabs-content')
])
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs-nav', 'value')
)
    
def render_content(tab):
    if tab == 'tab-1':
        return render_intro_tab()
    elif tab == 'tab-2':
        return render_hygiene_tab(finalizer)
    elif tab == 'tab-3':
        return render_stats_tab(finalizer_clean, raw_data_counts)
    elif tab == 'tab-4':
        return render_time_tab(finalizer_clean)
    elif tab == 'tab-5':
        return render_campaign_tab(finalizer_clean)
    elif tab == 'tab-6':
        return render_unit_tab(finalizer)       
    elif tab == 'tab-7':
        return render_performance_tab(finalizer_clean)
    elif tab == 'tab-8':
        return render_growth_tab(finalizer_clean)     
    elif tab == 'tab-9':
        return render_team_tab(finalizer_clean)     
    elif tab == 'tab-10':
        return render_conclusion_tab()
TAB_IDS = [f'tab-{i}' for i in range(1, 11)]
@app.callback(
    Output('tabs-nav', 'value'), 
    [Input('tabs-prev', 'n_clicks'), 
     Input('tabs-next', 'n_clicks')],
    State('tabs-nav', 'value')  
)
def switch_tab(prev_clicks, next_clicks, current_tab):
    
    triggered_id = ctx.triggered_id
    
    if not triggered_id or current_tab not in TAB_IDS:
        return current_tab
    
    current_index = TAB_IDS.index(current_tab)
    
    if triggered_id == 'tabs-prev' and current_index > 0:
        return TAB_IDS[current_index - 1]
    elif triggered_id == 'tabs-next' and current_index < len(TAB_IDS) - 1:
        return TAB_IDS[current_index + 1]
    
    return current_tab
        
    return html.Div("Tab not found")


if __name__ == '__main__':
   
    app.run(debug=True, port=8051)