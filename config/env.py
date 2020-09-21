import os
from dotenv import load_dotenv
load_dotenv()

os.environ.setdefault("ELASTICSEARCH_HOST", "localhost:9200")
os.environ.setdefault("ELASTICSEARCH_INDEX", 'snapshot')
os.environ.setdefault("CORENLP_HOST", "localhost:9000")
os.environ.setdefault("LOCAL_DATA_PATH", "./tests/")
os.environ.setdefault("LOCAL_DOWNLOAD_PATH", "./tests/")
os.environ.setdefault("DOWJONES_APIKEY", "3facdc19fc4d1dbd8a865a25239fe836")
os.environ.setdefault("DOWJONES_SNAPSHOTID", "3facdc19fc4d1dbd8a865a25239fe836")
