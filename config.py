import os


def get_env_or_default(key, default):
    env_var = os.environ.get(key)
    return default if env_var is None else env_var


server_url = get_env_or_default("TERMINUS_SERVER_URL", "http://localhost:6363")
key = get_env_or_default("TERMINUS_SERVER_PASS", "root")
db_id = get_env_or_default("TERMINUS_DB", "metrics")
