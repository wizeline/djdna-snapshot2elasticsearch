import json, config
from elasticsearch import Elasticsearch

les = Elasticsearch([config.elasticsearch_host])

with open('trading-news-mapping.json') as jxm_file:
    ixmap = json.load(jxm_file)
les.indices.create(index=config.elasticsearch_index, body=ixmap)

print("Index created!")
