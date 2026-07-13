from dash import dcc, html
import pandas as pd
from styles import TITLE_STYLE, SUBTITLE_STYLE, HEADER_WRAPPER


def render_hygiene_tab(finalizer):

    df = finalizer.get_data_hygiene_report()

    table_sections = []

    
    for table_name in df['Table'].unique():
        sub_df = df[df['Table'] == table_name].copy()
        cards = []

        for _, row in sub_df.iterrows():
            is_kept = row['Status'] == 'left'
            fill_rate = row['Filling_%']
            
            alpha = max(0.2, fill_rate / 100) 
            
            if is_kept:
                # Конвертуємо твій #6e6702 в RGB: (110, 103, 2)
                bg_color = f'rgba(110, 103, 2, {alpha})' 
                # Якщо фон став надто світлим (alpha < 0.5), ставимо темний текст
                final_text_color = '#2e2300' if alpha < 0.5 else 'white'
            else:
                bg_color = 'rgba(255, 215, 0, 1.0)' 
                final_text_color = '#2e2300'

            cards.append(html.Div([
                html.Div(row['Column'], style={
                    'fontSize': '11px', 
                    'fontWeight': 'bold', 
                    'height': '27px',           
                    'lineHeight': '1.2',
                    'color': final_text_color
                }),
                html.Div(f"{fill_rate}%", style={
                    'fontSize': '14px', 
                    'marginTop': '5px',          
                    'fontWeight': '900',
                    'color': final_text_color
                })
            ], style={
                'width': '110px',
                'height': '63px',               
                'padding': '9px',               
                'margin': '5px',
                'borderRadius': '8px',
                'backgroundColor': bg_color,
                'textAlign': 'center',
                'verticalAlign': 'top',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
                }))

        table_sections.append(html.Div([
            html.H4(f" Source: {table_name}", style={
                'borderLeft': '10px solid #6e6702',
                'paddingLeft': '15px',
                'margin': '20px 0 6px',
                'fontFamily': 'sans-serif'
            }),
            html.P(
                "Tile percent shows the share of records with a non-empty value in this column (column completeness).",
                style={'fontSize': '16px', 'color': '#333', 'margin': '0 0 8px 15px'}
            ),
            html.Div(
                cards,
                style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'flex-start'}
            )
        ]))

    return html.Div([
    html.Div([
        html.H2("Technical Data Audit Matrix", style=TITLE_STYLE),
        html.P(style=SUBTITLE_STYLE)
    ], style=HEADER_WRAPPER),

    html.Div(table_sections)
], style={'padding': '8px 16px'})
