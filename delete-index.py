import config
from elasticsearch import Elasticsearch

les = Elasticsearch([config.elasticsearch_host])

les.indices.delete(index=config.elasticsearch_index)

print("Index deleted!")
