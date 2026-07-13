BRAND_COLORS = {
    'gold': '#db9501', 'bronze': '#c05805', 'algae': '#6e6702',
    'bark': '#2e2300', 'crimson': '#8d230f', 'forest': '#1e434c', 'sage': '#a4ac86', 'maroon': '#800000'
}

TABS_STYLES = {
    'height': 'auto', 
    'minHeight': '45px', 
    'alignItems': 'stretch',
    'display': 'flex'
}

TAB_STYLE = {
    'padding': '6px 4px',
    'fontWeight': 600,
    'fontSize': '11px',
    'minHeight': '45px',
    'height': 'auto',
    'lineHeight': '1.2',  
    'whiteSpace': 'normal', 
    'textAlign': 'center',
    'display': 'flex',
    'alignItems': 'center',
    'justifyContent': 'center',
    'flex': '1',          
    'maxWidth': '120px'    
}

TAB_SELECTED_STYLE = {
    **TAB_STYLE,
    'color': 'white',
    'backgroundColor': BRAND_COLORS['forest'],
    'borderTop': f"3px solid {BRAND_COLORS['gold']}"
}
TITLE_STYLE = {
    'fontSize': '18px',
    'fontWeight': 700,
    'margin': '0',
    'color': BRAND_COLORS['bark']
}
SUBTITLE_STYLE = {
    'fontSize': '11px',
    'margin': '2px 0 8px',
    'color': BRAND_COLORS['bark'],
    'opacity': 0.85
}
HEADER_WRAPPER = {
    'padding': '6px 10px',
    'borderBottom': '1px solid #ddd',
    'marginBottom': '6px'
}
