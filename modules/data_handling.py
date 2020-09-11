import pandas as pd

def format_article_count(articles_count):
    data_list = [ 
        [ pd.to_datetime(article['key_as_string']) ,article['doc_count'] ]
        for article in articles_count
    ]

    return pd.DataFrame(data_list, columns=['date', 'count'])

def transform_dates(datesList):
    return [ pd.to_datetime(date) for date in datesList ]


