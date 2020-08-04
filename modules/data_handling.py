import pandas as pd
import datetime

def getArticleCountPerDay(articles):
    article_count_per_day = {}
    for article in articles:
        article_date = article['_source']['publication_date']//1000
        converted_date = datetime.datetime.fromtimestamp(article_date).date()
        article_count_per_day[converted_date] = article_count_per_day.get(converted_date, 0) + 1

    datesList = [ [date, article_count_per_day[date]] for date in article_count_per_day ]

    return pd.DataFrame(sorted(datesList), columns=['date', 'count']) 

def transformDates(datesList):
    return [ pd.to_datetime(date) for date in datesList ]