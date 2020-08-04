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
from modules.search import SearchClient

search_client = SearchClient(config.elasticsearch_host, config.elasticsearch_index)

with open('config/companies.json') as config_file:
    config_data = json.load(config_file)
    companies = { company['code'] : company for company in config_data['companies'] }
    terms = config_data['terms']
# companies = 
# terms = []

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    className='container',
	children = [
        html.H2('Travel monitoring'),
        dbc.InputGroup([
            dbc.InputGroupAddon('Select a company', addon_type='prepend'),
            dbc.Select(
                id='company',
                options=[ { 'label': companies[company]['name'], 'value' : companies[company]['code']  } for company in companies.keys() ],
                value=list(companies.keys())[0]
            )
        ], className='mb-3'),
        dbc.InputGroup([
            dbc.InputGroupAddon('Search', addon_type='prepend'),
            dbc.Input(
                id='search_input',
                type='search',
                className="form-control",
                placeholder='Search terms'
            ),
        ]),
        dcc.Graph(id='article_count_graph'),
        html.Div(
            children=[ html.Div(
                children=[ html.H5(term.capitalize()), dbc.Progress(value=25, id=term)]
            ) for term in terms ]
        )
    ]
)

@app.callback(
    [Output('article_count_graph', 'figure')] + [Output(term, 'value') for term in terms],
    [Input('company', 'value'), Input('search_input', 'value')]
)
def update_figure(selected_company, search_terms):
    ## Search for all the news of a company:
    company_all_articles = search_client.companySearch(selected_company)
    company_df = data_handling.getArticleCountPerDay(company_all_articles['hits'])

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=company_df['date'], 
            y=company_df['count'], 
            name='Total articles'
        )
    )

    # Get the term information
    total_articles = company_all_articles['total']['value']
    term_values = [ search_client.termCount(term, selected_company)*100/total_articles for term in terms ]
    

    # Get the stock information
    if companies[selected_company].get('ticker', 0) != 0:
        company_stocks = stock_handling.getTickerStocks(companies[selected_company]['ticker'])
        fig.add_trace(
            go.Scatter(
                x=data_handling.transformDates(company_stocks.index.values), y=company_stocks['High'], 
                name='Stock value',
                line=dict(color='blue')
            )
        )
    
    if search_terms:
        search_results = search_client.termSearch(search_terms, selected_company)
        df = data_handling.getArticleCountPerDay(search_results['hits'])
        fig.add_trace(
            go.Scatter(
                x=df["date"], 
                y=df["count"], 
                name='Term related count',
                line=dict(color='red')
            )
        )

    return (fig, *term_values)

if __name__ == '__main__':
	app.run_server(debug=True)
