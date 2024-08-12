import os


def get_config_env():
    config_dict = {"OPENAI_API_KEY": os.getenv("OPENAI_API_KEY")}
    return config_dict
