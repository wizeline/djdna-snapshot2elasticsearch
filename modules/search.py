from elasticsearch import Elasticsearch, ElasticsearchException

class SearchError(Exception):
    pass

class SearchClient():
    
    def __init__(self, elastic_host, index_name):
        self.elastic_client = Elasticsearch([elastic_host])
        self.index_name = index_name

    def term_search(self, keywords, companies):
        query = {
            "query": { 
                "bool" : {
                    "must" : [
                       {
                            "multi_match" : {
                               "query": keywords, "fields": [ "title","body"]
                            },
                       },
                        { "match" : { "company_codes": companies } }
                    ]
                }
            },
            "size" : "2500"
        }

        try:
            res = self.elastic_client.search(index=self.index_name, body=query)
            return res['hits']

        except ElasticsearchException:
            raise SearchError
    
    def company_search(self, companies):
        query = {
            "query" : {
                "match" : {
                    "company_codes" : companies
                }
            },
            "size" : "2500"
        }

        try:
            res = self.elastic_client.search(index=self.index_name, body=query)
            return res['hits']
        
        except ElasticsearchException:
            raise SearchError

    def term_count(self, term, companies):
        query = {
            "query": { 
                "bool" : {
                   "must" : [
                        { 
                            "multi_match" : 
                                { "query": term, "fields":[ "title","body"]
                            },
                        },
                        { "match" : { "company_codes": companies } }
                    ]
                }
            }
        }

        try:
            res = self.elastic_client.count(index=self.index_name, body=query)
            return res['count']
        except ElasticsearchException:
            raise SearchError
