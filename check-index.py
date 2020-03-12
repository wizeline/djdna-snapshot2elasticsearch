import config
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient

les = Elasticsearch([config.elasticsearch_host])

ixc = IndicesClient(client=les)
print(ixc.get_mapping(config.elasticsearch_index))
