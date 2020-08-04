import os, config
import djdna_common.snapshot_files as dna_ssf
import djdna_common.elasticsearch as dna_es
import djdna_common.enrichment as dna_ech

# This code asumes no authentication is enabled in ES
articles_folder = config.local_data_path
es_url = config.elasticsearch_host
es_index = config.elasticsearch_index
corenlp_host = config.corenlp_host

print("Starting")

for filename in sorted(os.listdir(articles_folder)):
    print("Reading file {}...".format(filename))
    # Loads multiple AVRO file articles to a single Pandas DataFrame
    file_articles = dna_ssf.read_file(articles_folder + filename, only_stats=False)
    print('Here!')
    compny_articles = file_articles[file_articles['company_codes_about'].ne('')].copy()
    compny_articles['body'] = compny_articles[['body']].apply(lambda x: '{}'.format(x[0]), axis=1)
    compny_articles['all'] = compny_articles['title'] + compny_articles['body']
    compny_articles['body'] = compny_articles['body']
    compny_articles = compny_articles.iloc[:2500]
    print("Done!\nEnriching title...", end='')

    # Enrich by adding an embedding to the title and body fields
    enriched_articles = dna_ech.add_embedding(compny_articles, 'title')
    print("Done!\nEnriching body...", end='')
    enriched_articles = dna_ech.add_embedding(enriched_articles, 'body')
    print("Done!\nEnriching All...", end='')
    enriched_articles = dna_ech.add_embedding(enriched_articles, 'all')
    # print("Done!\nCalculating CoreNLP Sentiment...", end='')
    # enriched_articles = dna_ech.add_corenlp_sentiment(enriched_articles, 'all', corenlp_host)
    print("Done!\nCalculating TextBlob Sentiment...", end='')
    enriched_articles = dna_ech.add_textblob_sentiment(enriched_articles, 'all')
    print("Done!\nLoading to Elasticsearch...", end='')

    # Loads articles to Elasticsearch
    enriched_articles.drop(columns=['all'], inplace=True)
    total_saved = dna_es.save_articles(es_url, es_index, enriched_articles)
    print('Done!\nSaved {} articles to the index {}, located in the server {}'.format(
          total_saved, es_index, es_url))
