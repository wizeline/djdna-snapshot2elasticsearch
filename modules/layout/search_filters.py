import dash_core_components as dcc
import dash_html_components as html

search_bar = (
    html.Div([
        html.Div([
            html.Label('Search for terms in the news', className='mdc-typography--subtitle1 mdc-theme--secondary'),
        ], className='mdc-layout-grid__cell--span-12'),
        html.Div([
            html.Label([
                html.I('search', className='material-icons mdc-text-field__icon mdc-text-field__icon--leading mdc-theme--primary', tabIndex='0', role='button'),
                html.Span(className='mdc-text-field__ripple'),
                dcc.Input(type='text', className='mdc-text-field__input', id='search_input'),
                html.Span(className='mdc-line-ripple', style={ 'color' : 'red' })    
            ], className='mdc-text-field mdc-text-field--filled mdc-text-field--with-leading-icon mdc-text-field--fullwidth')
        ], className='mdc-layout-grid__cell--span-10'),
        html.Div([
            html.Button([
                html.Span('SEARCH', className='mdc-button__label')
            ], className='mdc-button mdc-button--raised', style={'display' : 'flex', 'width' : '100%'})
        ], className='mdc-layout-grid__cell--span-2-desktop mdc-layout-grid__cell--span-12-tablet'),
    ], className='mdc-layout-grid__inner')
)

def create_company_select(companies):
    return html.Div([
        html.Label(
        'Select the companies to monitor in the news', 
        className='mdc-typography--subtitle1 mdc-theme--secondary'),
        dcc.Dropdown(
            options = [ { 'label': companies[company]['name'], 'value' : companies[company]['code']  } for company in companies.keys() ],
            value=list(companies.keys())[0],
            multi=True,
            id='company-filter')
    ])
