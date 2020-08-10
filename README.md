# Elasticsearch Sample Dashboard


Sample Dash App to read snapshots data loaded into Elasticsearch. The app includes ploting article counts per day, free search and article preview.

Additional files are included to create and download snapshots files, and to load and enrich the files into elasticsearch.


## Dependencies
- Library dependencies for Python are listed on `requirements.txt`.
- Methods from the [djdna_common](https://github.com/miballe/djdna_common) library are used. 

    The **djdna_common** library is a set of common methods that eases operations like reading DNA Snapshots AVRO files, calculating new features or interacting with Elasticsearch. These methods are for illustration purposes and don't have a robust coding to validate unexpected cases or handling exceptions. For this reason it is not distributed as a Python package. It is however used among multiple Dow Jones DNA examples.

    To use these methods, clone this and the djdna_common repository to the same base directory, and (if necessary) create a symbolic link or copy the folder content. A sample sequence looks like this:

    ```
    $ git clone https://github.com/miballe/djdna-snapshot2elasticsearch.git
    $ git clone https://github.com/miballe/djdna_common
    $ cd djdna-snapshot2elasticsearch
    $ ln -s ../djdna_common/ djdna_common
    ```

- Methods from the [factiva_common](https://github.com/dowjones/factiva_common) are used.

    To use these methods, clone the **factiva_common** repository to the same base directory, and create a symbolic link or copy the folder content, like this:

    ```
    $ git clone https://github.com/dowjones/factiva_common
    $ ln -s ../factiva_common/ factiva_common
    ```

- Elasticsearch server. To set an elasticsearch server please refer to [the official documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html).

    It is required to create an index before running the application. You can run the `create_index.py` to create it. You can choose to do it manually, if so, remember to add the mapping included in `resources/files/dna-es-mappings.json`.

- CoreNLP Server. This server is used to enrich the contents before loading them into elastisearch. Please refer to the [official website](https://stanfordnlp.github.io/CoreNLP/corenlp-server.html) to gather information on setting it up.


## Running the application

1. Fill out the `config/env.py` file.

2. Create a snapshot and download the resulting articles. 

    - If you don't have a created snapshot, you can use the `create-snapshot.py` file. Add your query to this file. This will create the snapshot and download the files.

    - If you have created snapshot you can use the `article-download.py` file. This will download the files for the `snapshot_id` specified on the `config/env.py`. 

3. Create the elasticsearch index by running `create_index.py`. You can choose do to so manually, if so, remember to add the mapping included in `resources/files/dna-es-mappings.json`.

4. Load the data into elasticsearch by running `load-dna-data.py`

5. Run the app with `main.py`
