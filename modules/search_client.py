from elasticsearch import Elasticsearch, ElasticsearchException

class SearchError(Exception):
    pass

class SearchClient():
    
    def __init__(self, elastic_host, index_name):
        self.elastic_client = Elasticsearch([elastic_host])
        self.index_name = index_name

    def execute_search(self, query):
        try:
            return self.elastic_client.search(index=self.index_name, body=query)
        except ElasticsearchException as e:
            print(e)
            raise SearchError
    
    def count(self, query):
        try:
            return self.elastic_client.count(index=self.index_name, body=query)
        except ElasticsearchException:
            raise SearchError
    
    def get_term_sentiment_average_per_company(self, term, companies):
        query = {
            "size": 0,
            "query" : { 
                "multi_match" : { "query": term, "fields":[ "title","body"] }
            },
            "aggs": { 
                company_code : {
                    "filter" : { "term" : { "company_codes" : company_code } },
                    "aggs" : { 
                        "sentiment_avg" : { "avg": { "field": "textblob_sentiment_score" } }
                    }
                } for company_code in companies
            }
        }
    
        res = self.execute_search(query)
        return { company_code : res['aggregations'][company_code]['sentiment_avg']['value'] for company_code in companies }

    def get_article_count_per_day(self, companies, terms):
        query={
            'size' : 0,
            'aggs': {
                'count_per_day': {
                    'date_histogram': {
                        'field': 'publication_date',
                        'calendar_interval': 'day',
                        'format': 'yyyy-MM-dd'
                    }
                }
            }
        }

        if terms:
            query['query'] = {
                'bool' : {
                   'must' : [
                        { 'multi_match' : { 'query': terms, 'fields':[ 'title', 'body'] } },
                        { 'match' : { 'company_codes' : companies } }
                    ]
                }
            }
        else:
            query['query'] = { 'match' : { 'company_codes' : companies } }

        res = self.execute_search(query)
        return res['aggregations']['count_per_day']['buckets']

    def term_search(self, keywords, companies):
        query = {
            "query": { 
                "bool" : {
                    "must" : [
                       { "multi_match" : { "query": keywords, "fields": [ "title","body"] } },
                       { "match" : { "company_codes": companies } }
                    ]
                }
            },
            "size" : "10"
        }

        res = self.execute_search(query)
        return res['hits']['hits']

    
    def company_search(self, companies):
        query = {
            'query' : { 'match' : { 'company_codes' : companies } },
            'size' : '10'
        }

        res = self.execute_search(query)
        return res['hits']['hits']

    def company_article_count(self, companies):
        query = {
            'query' : {
                'match' : { 'company_codes' : companies }
            }
        }

        res = self.count(query)
        return res['count'] 


    def term_count(self, term, companies):
        query = {
            'query': { 
                'bool' : {
                   'must' : [
                        { 
                            'multi_match' : 
                                { 'query': term, 'fields':[ 'title', 'body']
                            },
                        },
                        { 'match' : { 'company_codes' : companies } }
                    ]
                }
            }
        }

        res = self.count(query)
        return res['count']