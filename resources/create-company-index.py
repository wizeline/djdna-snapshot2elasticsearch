import config
import djdna_common.elasticsearch as dna_es
import datetime
import json
from elasticsearch import Elasticsearch


# This code asumes no authentication is enabled in ES
es_url = config.elasticsearch_host
es_index = config.elasticsearch_index
companies_index = 'companies'

es_client = Elasticsearch([es_url])

companies = json.load(open('../config/companies.json'))
companies = companies['companies']

for company in companies:
    query = {
        "query": {
            "query_string" : {
                "query" : "company_codes:{} AND (title:((resort* OR restaurant* OR fast food OR hotel* OR casino$) AND (difficult* OR auction OR bankruptcy OR debt OR distressed sale OR foreclos* OR receivership OR declin* OR food poisoning OR botulism OR salmonella OR e coli OR cleanliness OR traffic congestion OR crime OR trouble* OR problem$ OR malaise OR slowdown) OR ((clos* OR shutter* OR struggl* OR beleaguer*) AND (hotel* OR resort* OR restaurant* OR fast food OR casino*)) OR ((traveler* OR tourist* OR customer*) AND (spending OR sentiment OR booking* OR reservation* ) AND (slowdown OR weak* OR low* or less*))) OR body:(sales AND (sluggish OR fell OR fall* OR decreas* OR declin* OR drop* OR slump* OR stumbl* OR slid* OR lagg*)))".format(company['code'])
            }
        },
        "size" : 1000,
        "sort" : [
            { "publication_date" : {"order" : "asc"} } ],
    }

    res = es_client.search(index=es_index, body=query)
    total_results = res['hits']['total']['value']
    print("Got %d Hits" %total_results )

    article_count_per_day = {}

    for hit in res['hits']['hits']:
        hit_date = hit['_source']['publication_date']//1000
        converted_date = datetime.datetime.fromtimestamp(hit_date).date()
        article_count_per_day[converted_date] = article_count_per_day.get(converted_date, 0) + 1

    company_info = {
        "company_code" : company['name'],
        "article_counts" : [ { "date" : date, "article_count" : article_count_per_day[date] } for date in article_count_per_day ]
    }

    res = es_client.index(index=companies_index, body=company_info, id=company['code'])
    print(res['result'])