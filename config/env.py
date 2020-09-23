import os
from dotenv import load_dotenv
load_dotenv()

os.environ.setdefault("ELASTICSEARCH_HOST", "")
os.environ.setdefault("ELASTICSEARCH_INDEX", "")
os.environ.setdefault("CORENLP_HOST", "")
os.environ.setdefault("LOCAL_DATA_PATH", "")
os.environ.setdefault("LOCAL_DOWNLOAD_PATH", "")
os.environ.setdefault("DOWJONES_APIKEY", "")
os.environ.setdefault("DOWJONES_SNAPSHOTID", "")
