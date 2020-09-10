import dash_html_components as html
from modules.ui.modal import Modal
from datetime import datetime

container = (
    html.Div([
        html.Label('Top hits', className='mdc-typography--subtitle1 mdc-theme--secondary'),
        html.Div(id='article_list')
    ])
)

load_more_button = (
    html.Div([
        html.Button([
                html.Span('LOAD MORE', className='mdc-button__label')
            ], className='mdc-button mdc-button--raised', id='load_more_button')
    ], className='mdc-layout-grid__cell--span-12', style={ 'text-align' : 'center', 'padding' : '30px'})
)

def create_article_list_layout(article_list):
    return html.Ul([
            html.Li([
                html.Span(className='mdc-list-item__ripple'),
                html.Span([
                    html.Span([
                        article['_source']['title']
                    ], className = ('mdc-list-item__primary-text')),
                    html.Span([
                        get_publication_date(article['_source']['publication_date'])
                    ], className='mdc-list-item__secondary-text')
                ], className='mdc-list-item__text'),
                Modal(article['_source']['title'], article['_source']['body'], i).create()
            ], className='mdc-list-item mdc-divider-bottom', id={'index' : i, 'role' : 'open'}) for i, article in enumerate(article_list)
        ], className='mdc-list mdc-list--two-line mdc-divider-top')

def get_publication_date(date):
    formatted_date = datetime.fromtimestamp(date/1000)
    return formatted_date.strftime('%b %d %Y %I:%M %p')
