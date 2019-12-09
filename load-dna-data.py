import djdna_common.snapshot_files as dna_ssf
import djdna_common.elasticsearch as dna_es
import djdna_common.enrichment as dna_ech

# This code asumes no authentication is enabled in ES
articles_folder = "../articles-avro/"
es_url = 'http://localhost:9200'
es_index = 'dnaarticles'

# Loads multiple AVRO file articles to a single Pandas DataFrame
sample_articles = dna_ssf.read_folder(articles_folder, only_stats=False)

# Enrich by adding an embedding to the title and body fields
enriched_articles = dna_ech.add_embedding(sample_articles, 'title')
enriched_articles = dna_ech.add_embedding(enriched_articles, 'body')

# Loads articles to Elasticsearch
total_saved = dna_es.save_articles(es_url, es_index, sample_articles)
print('Saved {} articles to the index {}, located in the server {}'.format(
  total_saved, es_index, es_url))
