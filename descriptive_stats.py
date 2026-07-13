import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash import html, dcc, dash_table
import pandas as pd
from styles import BRAND_COLORS, TITLE_STYLE, SUBTITLE_STYLE, HEADER_WRAPPER
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def prettify_labels(s: pd.Series) -> pd.Series:
    s = pd.Series(s).fillna('Unknown').astype(str)
    s = s.str.strip()
    s = s.str.replace('_', ' ', regex=False).str.replace('-', ' ', regex=False)
    s = s.str.replace(r'\s+', ' ', regex=True)
    return s.str.title()

def render_stats_tab(finalizer, raw_data_counts):
    d1 = finalizer.d1
    d2 = finalizer.d2

    cols_stats = ['initial_amount_paid', 'offer_total_amount', 'sla_min']
    existing_cols = [c for c in cols_stats if c in d1.columns]
    
    if existing_cols:
        desc_df = d1[existing_cols].describe().reset_index().round(2)
    else:
        desc_df = pd.DataFrame({"Message": ["No numerical columns found"]})

  
    def safe_get_counts(df, col_name, val_col=None):
        try:
            if col_name not in df.columns:
                return pd.DataFrame(columns=['category', 'value'])
            
            temp = df.copy()
            temp[col_name] = temp[col_name].fillna('unknown').astype(str)
            
            if val_col and val_col in temp.columns:
                res = temp.groupby(col_name)[val_col].sum().sort_values().tail(10).reset_index()
            else:
                res = temp[col_name].value_counts().sort_values().tail(10).reset_index()
            
            res.columns = ['category', 'value']
            return res
        except:
            return pd.DataFrame(columns=['category', 'value'])


    fig_cats = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Lost Reasons (d1)",
            "Deal Stages (d1)",
            "Spend by Source (d2)",
            "Deals by Source (d1)"
        ),
        horizontal_spacing=0.08,
        vertical_spacing=0.10
    )

    # 1) Lost Reasons
    c1 = safe_get_counts(d1, 'lost_reason')
    c1['category_pretty'] = c1['category'].fillna('Unknown').astype(str).str.strip().str.title()
    fig_cats.add_trace(
        go.Bar(x=c1['value'], y=c1['category_pretty'], orientation='h',
               marker_color=BRAND_COLORS.get('forest', '#1e434c')),
        row=1, col=1
    )
    order1 = c1.sort_values('value')['category_pretty'].tolist()
    fig_cats.update_yaxes(categoryorder='array', categoryarray=order1, row=1, col=1)

    # 2) Deal Stages
    c2 = safe_get_counts(d1, 'stage')
    c2['category_pretty'] = prettify_labels(c2['category'])
    fig_cats.add_trace(
        go.Bar(x=c2['value'], y=c2['category_pretty'], orientation='h',
               marker_color=BRAND_COLORS.get('sun', '#f6ae2d')),
        row=1, col=2
    )
    order2 = c2.sort_values('value')['category_pretty'].tolist()
    fig_cats.update_yaxes(categoryorder='array', categoryarray=order2, row=1, col=2)

    c3 = safe_get_counts(d2, 'source', val_col='spend')
    c3['category_pretty'] = prettify_labels(c3['category'])
    fig_cats.add_trace(
        go.Bar(x=c3['value'], y=c3['category_pretty'], orientation='h',
               marker_color=BRAND_COLORS.get('bark', '#8d230f')),
        row=2, col=1
    )
    order3 = c3.sort_values('value')['category_pretty'].tolist()
    fig_cats.update_yaxes(categoryorder='array', categoryarray=order3, row=2, col=1)

   
    c4 = safe_get_counts(d1, 'source')
    c4['category_pretty'] = prettify_labels(c4['category'])
    fig_cats.add_trace(
        go.Bar(x=c4['value'], y=c4['category_pretty'], orientation='h',
               marker_color=BRAND_COLORS.get('copper', '#b87333')),
        row=2, col=2
    )
    order4 = c4.sort_values('value')['category_pretty'].tolist()
    fig_cats.update_yaxes(categoryorder='array', categoryarray=order4, row=2, col=2)

    fig_cats.update_layout(
        bargap=0.50,
        template='plotly_white',
        margin=dict(l=10, r=10, t=30, b=10),
        height=800,
        showlegend=False
    )
    fig_cats.update_yaxes(automargin=True)
    fig_cats.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.06)')
    fig_cats.update_traces(marker_opacity=0.85, marker_line_width=0, selector=dict(type='bar'))
    fig_cats.update_annotations(font=dict(size=14, color=BRAND_COLORS.get('bark', '#333')))

   
    amount_col = 'initial_amount_paid'
    s = pd.to_numeric(d1[amount_col], errors='coerce')
    s = s[(s > 0)].dropna()

    if not s.empty:
        q1, q2, q3 = s.quantile([0.25, 0.5, 0.75])
        iqr = q3 - q1
        min_, max_ = float(s.min()), float(s.max())
        lf = q1 - 1.5 * iqr
        uf = q3 + 1.5 * iqr
        out_share = float(((s < lf) | (s > uf)).mean())

        col_all = BRAND_COLORS.get('copper', '#b87333')
        maroon = BRAND_COLORS.get('maroon', '##800000')
        
        fig_strip = px.strip(
            x=s,
            orientation='h',
            color_discrete_sequence=[col_all],
        )
        fig_strip.update_traces(
            jitter=0.25,
            marker=dict(size=4, opacity=0.55, color=col_all),
            hovertemplate='Value: %{x:,.0f}<extra></extra>'
        )

        marks = [
            (min_, 'min', 'solid'),
            (q1, 'Q1', 'solid'),
            (q2, 'Median', 'solid'),
            (q3, 'Q3', 'solid'),
            (max_, 'max', 'solid'),
        ]

        for x_val, name, dash in marks:
            width = 1.0 if name == 'Median' else 0.8
            fig_strip.add_vline(x=float(x_val), line_width=width, line_dash=dash, line_color=col_all)
            fig_strip.add_annotation(
                x=float(x_val), y=1.06, xref='x', yref='paper',
                text=f"{name}: {x_val:,.0f}", showarrow=False,
                textangle=0, xanchor='center', yanchor='bottom',
                font=dict(size=10, color= "maroon"), bgcolor='rgba(255,255,255,0.7)'
            )

        fig_strip.update_layout(
            paper_bgcolor='#f5f5f7', plot_bgcolor='#f5f5f7',
            title=f"Initial Payments — Distribution Across All Deals, 2023–2024", title_x=0.5,
            template='plotly_white', height=460,
            margin=dict(l=120, r=20, t=120, b=40),
            font=dict(size=12),
            hoverlabel=dict(
            bgcolor='white',           # білий фон тултіпу
            bordercolor='#d0d0d0',     # світло-сіра рамка
            font=dict(color='#333', size=11)  # темно-сірий текст
        ))
        fig_strip.update_xaxes(title='Initial amount paid', tickformat=',.0f', title_standoff=8)
        fig_strip.update_yaxes(visible=False, showticklabels=False)
        fig_box = fig_strip
    else:
        fig_box = go.Figure().update_layout(title="No data for payments")

    # --- Повернення Layout ---
    return html.Div([
        html.Div([
            html.H2("Descriptive Analytics: Cleaned Data Overview", style=TITLE_STYLE)
        ], style=HEADER_WRAPPER),

        html.Div([
            dash_table.DataTable(
                data=desc_df.to_dict('records'),
                columns=[{"name": i, "id": i} for i in desc_df.columns],
                style_header={'backgroundColor': BRAND_COLORS['bark'], 'color': 'white', 'fontWeight': 'bold'},
                style_cell={'textAlign': 'center', 'fontFamily': 'sans-serif'}
            )
        ], style={'margin': '20px'}),

        dcc.Graph(figure=fig_box, style={'border': '1px solid #e6e6e6', 'borderRadius': '8px', 'background': '#f5f5f7'}),
        dcc.Graph(figure=fig_cats)
    ])