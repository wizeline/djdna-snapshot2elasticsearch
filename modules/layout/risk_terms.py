import dash_html_components as html
import dash_core_components as dcc

from itertools import chain

from modules.ui.progress import Progress

container = (
    html.Div([
        html.Label('Percentage of articles with Risk terms', className='mdc-typography--subtitle1 mdc-theme--secondary'),
        html.Div(id='risk-terms-count', className='mdc-layout-grid__inner mdc-typography mdc-theme--on-surface')
    ])
)

def get_risk_term_layout(companies, selected_companies, terms, terms_values, term_sentiment_average ):
    terms_information = {}
    for i, term in enumerate(terms):
        terms_information[term] = { 
            'percentage' : terms_values[i],
            'sentiment' : term_sentiment_average[i]
        }

    return [
            html.Div(className='mdc-layout-grid__cell--span-6'),
            html.Div([
                html.Div([
                    html.Div(
                        companies[company_code]['name'], 
                        className='mdc-layout-grid__cell--span-2',
                        style={ 'white-space': 'nowrap', 'overflow': 'hidden', 'text-overflow': 'ellipsis' }
                    ) for company_code in selected_companies
                ], className='mdc-layout-grid__inner')
            ], className='mdc-layout-grid__cell--span-6'),
            html.Div([
                html.Div(list(chain.from_iterable(
                    (
                        html.Div([
                            term.capitalize()
                        ], className='mdc-layout-grid__cell--span-2'),
                        html.Div([
                            Progress( (terms_information[term]['percentage'])/100 ).create()
                        ], className='mdc-layout-grid__cell--span-3', style={'margin-top' : '3%'}),
                        html.Div([
                            '{:.2f}%'.format(terms_information[term]['percentage'])
                        ], className='mdc-layout-grid__cell--span-1'),
                        html.Div([
                            html.Div([
                                html.Div(
                                    '{:.2f}'.format(terms_information[term]['sentiment'][company_code]),
                                    className='mdc-layout-grid__cell--span-2', 
                                    style={
                                        'text-align' : 'center',
                                        'color' : 'red' if terms_information[term]['percentage'] < 0 else 'green'
                                    },
                                ) for company_code in selected_companies
                            ], className='mdc-layout-grid__inner')
                        ], className='mdc-layout-grid__cell--span-6')
                    ) for term in terms_information
                )), className='mdc-layout-grid__inner')
            ], className='mdc-layout-grid__cell--span-12'),
        ]
