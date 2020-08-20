import json
import config
import os
from elasticsearch import Elasticsearch

les = Elasticsearch([config.elasticsearch_host])

with open(os.path.join('resources/files', 'dna-es-mappings.json')) as jxm_file:
    ixmap = json.load(jxm_file)
les.indices.create(index=config.elasticsearch_index, body=ixmap)

print("Index created!")
