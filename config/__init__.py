import os


def load_env_config_value(config_key):
    tmp_val = os.getenv(config_key, None)
    if tmp_val is None:
        raise Exception("Environment Variable {} not found!".format(config_key))
    return tmp_val


elasticsearch_host = load_env_config_value("ELASTICSEARCH_HOST")
elasticsearch_index = load_env_config_value("ELASTICSEARCH_INDEX")
corenlp_host = load_env_config_value("CORENLP_HOST")
local_data_path = load_env_config_value("LOCAL_DATA_PATH")
