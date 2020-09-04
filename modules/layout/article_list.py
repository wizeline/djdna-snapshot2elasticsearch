import dash_html_components as html
from modules.ui.modal import Modal
from datetime import datetime

container = (
    html.Div([
        html.Label('Top hits', className='mdc-typography--subtitle1 mdc-theme--secondary'),
        html.Div(id='article_list')
    ])
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
    return str(datetime.fromtimestamp(date/1000))
