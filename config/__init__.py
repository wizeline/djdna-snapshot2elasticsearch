import os
from . import env
import json


def load_env_config_value(config_key):
    tmp_val = os.getenv(config_key, None)
    if tmp_val is None:
        raise Exception("Environment Variable {} not found!".format(config_key))
    return tmp_val

def load_companies():
    with open('config/companies.json') as config_file:
        config_data = json.load(config_file)
        companies = { company['code'] : company for company in config_data['companies'] }
        return companies

def load_terms():
    with open('config/companies.json') as config_file:
        config_data = json.load(config_file)
        terms = config_data['terms']
        return terms

elasticsearch_host = load_env_config_value("ELASTICSEARCH_HOST")
elasticsearch_index = load_env_config_value("ELASTICSEARCH_INDEX")
corenlp_host = load_env_config_value("CORENLP_HOST")
local_data_path = load_env_config_value("LOCAL_DATA_PATH")
local_download_path = load_env_config_value("LOCAL_DOWNLOAD_PATH")
dowjones_apikey = load_env_config_value("DOWJONES_APIKEY")
dowjones_snapshotid = load_env_config_value("DOWJONES_SNAPSHOTID")
