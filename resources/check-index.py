from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
import config

les = Elasticsearch([config.elasticsearch_host])

ixc = IndicesClient(client=les)
print(ixc.get_mapping(config.elasticsearch_index))
