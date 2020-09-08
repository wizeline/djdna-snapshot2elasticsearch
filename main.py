import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

import config
from app import app 

import modules.data_handling as data_handling
import modules.stock_client as stock_client

import modules.layout.header as Header
import modules.layout.risk_terms as RiskTerms
import modules.layout.search_filters as SearchFilters
import modules.layout.footer as Footer
import modules.layout.article_list as ArticleList

from dash.dependencies import Input, Output, State
from modules.search_client import SearchClient, SearchError
from modules.ui.modal import set_toggle_modal, Modal


search_client = SearchClient(config.elasticsearch_host, config.elasticsearch_index)

companies = config.load_companies()
terms = config.load_terms()

color_pool = ['navy', 'blue', 'purple', 'pink', 'indigo', 'slateblue', 'turqouise', 'chocolate', 'cyan', 'hotpink']

app.layout = html.Div([
    html.Div([
        Header.logo_header,
        html.Div([
            html.Div([
                Header.title
            ], className='mdc-layout-grid__cell--span-12'),
            html.Div([
                SearchFilters.create_company_select(companies),
                SearchFilters.search_bar,
            ], className='mdc-layout-grid__cell--span-6 mdc-layout-grid__cell--align-middle'),
            html.Div([
                RiskTerms.container
            ], className='mdc-layout-grid__cell--span-6'),
            html.Div([
                dcc.Graph(id='article_count_graph')
            ], className='mdc-layout-grid__cell--span-12'),
            html.Div([
                ArticleList.container
            ], className='mdc-layout-grid__cell--span-12')
        ], className='mdc-layout-grid__inner'),
        Footer.footer
    ], className='mdc-layout-grid')
])

# Set modal callback
set_toggle_modal(app)


@app.callback(
    Output('risk-terms-count', 'children'),
    [ Input('company-filter', 'value') ]
)
def get_risk_term_section(selected_companies):
    if isinstance(selected_companies, str):
        selected_companies = [ selected_companies ]

    companies_to_search = ' '.join(selected_companies)

    try:
        total_articles = search_client.company_article_count(companies_to_search)

        if total_articles == 0:
            return 'No articles found'
        
        term_values = [ search_client.term_count(term, companies_to_search)*100/total_articles for term in terms ]

        sentiment_average = [ 
            search_client.get_term_sentiment_average_per_company(term, selected_companies) for term in terms
        ]

        return RiskTerms.get_risk_term_layout(companies, selected_companies, terms, term_values, sentiment_average)
        
    except SearchError:
        return 'An error ocurred'
   
@app.callback(
    Output('article_count_graph', 'figure'), 
    [ Input('company-filter', 'value'), Input('search_button', 'n_clicks') ],
    [ State('search_input', 'value') ]
)
def update_figure(selected_companies, n_clicks, search_terms):
    if isinstance(selected_companies, str):
        selected_companies = [ selected_companies ]

    companies_to_search = ' '.join(selected_companies)

    fig = go.Figure(layout=go.Layout(dragmode='pan'))

    try:
        article_count = search_client.get_article_count_per_day(companies_to_search, None)   
    except SearchError:
        return fig

    formatted_data = data_handling.format_article_count(article_count) 
    fig.add_trace(
        go.Bar( x=formatted_data['date'], y=formatted_data['count'], name='Total articles')
    )

    # Get the stock information
    for index, company in enumerate(selected_companies):
        if 'ticker' in companies[company]:
            company_stocks = stock_client.get_ticker_stocks(companies[company]['ticker'])
            fig.add_trace(
                go.Scatter(
                    x=data_handling.transform_dates(company_stocks.index.values), 
                    y=company_stocks['High'], 
                    name='{} stock value'.format(companies[company]['name']),
                    line=dict(color=color_pool[index])
                
                )
            )

    if search_terms:
        try:
            search_term_article_count = search_client.get_article_count_per_day(companies_to_search, search_terms)
        except SearchError:
            return fig

        search_term_formatted_data = data_handling.format_article_count(search_term_article_count) 
        fig.add_trace(
            go.Scatter(
                x=search_term_formatted_data["date"], 
                y=search_term_formatted_data["count"], 
                name='Term related count',
                line=dict(color='red')
            )
        )
    
    return fig

@app.callback(
    Output('article_list', 'children'),
    [ Input('company-filter', 'value'), Input('search_button', 'n_clicks') ],
    [ State('search_input', 'value') ]
)
def update_article_list(selected_companies, n_clicks, search_terms):
    if isinstance(selected_companies, str):
        selected_companies = [ selected_companies ]

    companies_to_search = ' '.join(selected_companies)

    article_list = []

    try:
        if search_terms is None:
            article_list = search_client.company_search(companies_to_search)
        else:
            article_list = search_client.term_search(search_terms, companies_to_search)
        
    except SearchError:
        return 'An error ocurred'
    
    return ArticleList.create_article_list_layout(article_list)

if __name__ == '__main__':
	app.run_server(debug=True)
