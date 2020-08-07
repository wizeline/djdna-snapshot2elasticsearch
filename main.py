import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import json
import config

import modules.data_handling as data_handling
import modules.stock_handling as stock_handling

from dash.dependencies import Input, Output
from modules.search import SearchClient, SearchError
from modules.progress import Progress
from modules.modal import set_toggle_modal
from modules.list_item import ListItem

search_client = SearchClient(config.elasticsearch_host, config.elasticsearch_index)

with open('config/companies.json') as config_file:
    config_data = json.load(config_file)
    companies = { company['code'] : company for company in config_data['companies'] }
    terms = config_data['terms']

external_stylesheets = [dbc.themes.BOOTSTRAP]

color_pool = ['navy', 'blue', 'purple', 'pink', 'indigo', 'slateblue', 'turqouise', 'chocolate', 'cyan', 'hotpink']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    className='container',
	children = [
        html.H2('Travel monitoring'),
        dbc.Alert('A search error has ocurred', color='danger', is_open=False, id='error'),
        dbc.FormGroup([
            
            dbc.Label('Select companies', html_for='company'),
            dcc.Dropdown(
                options = [ { 'label': companies[company]['name'], 'value' : companies[company]['code']  } for company in companies.keys() ],
                value=list(companies.keys())[0],
                multi=True,
                id='company'
            ),
        
        ], className='mb-3'),
        dbc.InputGroup([
            dbc.InputGroupAddon('Search', addon_type='prepend'),
            dbc.Input(
                id='search_input',
                type='search',
                className="form-control",
                placeholder='Search terms'
            ),
        ], className='mb-3'),
        dbc.Row([
            dbc.Col(html.Div([ Progress(term, 0).create() for term in terms ]), width=6),
            dbc.Col([
                html.H5('Credit risk score'),
                html.Div(id='companies_score'),
            ], width=6 )
        ]),
        dcc.Graph(id='article_count_graph'),
        html.H3('Top hits'),
        dbc.ListGroup(id='article_list',  className='mb-3')
    ]
)

# Adding the modal's callback
set_toggle_modal(app)

@app.callback(
    [
        Output('error', 'is_open'),
        Output('article_count_graph', 'figure'), 
        Output('article_list', 'children'),
        Output('companies_score', 'children')
    ] + [Output(term, 'value') for term in terms],
    [ Input('company', 'value'), Input('search_input', 'value') ]
)
def update_figure(selected_companies, search_terms, *args):
    selected_companies = [ selected_companies ] if isinstance(selected_companies, str) else selected_companies
    companies_to_search = ' '.join(selected_companies)

    ## Search for all the news of a company:
    try:
        company_all_articles = search_client.company_search(companies_to_search)
    except SearchError:
        return (True, go.Figure(), [], [], *([0] * len(terms)) )

    company_df = data_handling.get_article_count_per_day(company_all_articles['hits'])

    # Calculate risk score
    sentiment_result = [ ]
    for company in selected_companies:
        company_articles = search_client.company_search(company)
        sentiment_result.append(
            html.P(
                '{} : {:.2f}'.format(
                    companies[company]['name'], 
                    data_handling.get_sentiment_average(company_articles['hits'])
                ) 
            )
        )

    resulting_articles = [ 
        ListItem( 
            article['_source']['title'],
            article['_source']['body'], 
            index
        ).create() for index, article in enumerate(company_all_articles['hits'][:10]) 
    ]

    fig = go.Figure(layout=go.Layout(dragmode='pan'))
    fig.add_trace(
        go.Bar(
            x=company_df['date'], 
            y=company_df['count'], 
            name='Total articles',
        )
    )
    
    # Get the term information
    total_articles = company_all_articles['total']['value']
    try:
        term_values = [ search_client.term_count(term, companies_to_search)*100/total_articles for term in terms ]
    except (SearchError, ZeroDivisionError):
        return (True, go.Figure(), [], sentiment_result, *([0] * len(terms)) )

    # Get the stock information
    for index, company in enumerate(selected_companies):
        if 'ticker' in companies[company]:
            company_stocks = stock_handling.get_ticker_stocks(companies[company]['ticker'])
            fig.add_trace(
                go.Scatter(
                    x=data_handling.transform_dates(company_stocks.index.values), y=company_stocks['High'], 
                    name='{} stock value'.format(companies[company]['name']),
                    line=dict(color=color_pool[index])
                )
            )
    
    if search_terms:
        try:
            search_results = search_client.term_search(search_terms, companies_to_search)
        except SearchError:
            return (True, fig, resulting_articles, sentiment_result, *term_values)

        df = data_handling.get_article_count_per_day(search_results['hits'])
        resulting_articles = [ 
            ListItem( 
                article['_source']['title'],
                article['_source']['body'], 
                index
            ).create() for index, article in enumerate(search_results['hits'][:10]) 
        ]
        fig.add_trace(
            go.Scatter(
                x=df["date"], 
                y=df["count"], 
                name='Term related count',
                line=dict(color='red')
            )
        )

    return (False, fig, resulting_articles, sentiment_result, *term_values)

if __name__ == '__main__':
	app.run_server(debug=True)
