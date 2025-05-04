from typing import Dict

from decouple import config


def export_splunk_config() -> Dict[str, str]:
    """
    Export the Splunk configuration as a dictionary.

    Returns:
        A dictionary with the Splunk configuration keys and values.
    """
    return {
        "SPLUNK_HOST": config("SPLUNK_HOST"),
        "SPLUNK_PORT": config("SPLUNK_PORT"),
        "SPLUNK_TOKEN": config("SPLUNK_TOKEN"),
        "SPLUNK_AUTO_LOGIN": config("SPLUNK_AUTO_LOGIN", default=True, cast=bool),
    }


def export_db_config() -> Dict[str, str|int]:
    """
    Export the database configuration as a dictionary.

    Returns:
        A dictionary with the database configuration keys and values.
    """
    return {
        "DB_HOST": config("DB_HOST"),
        "DB_PORT": config("DB_PORT", cast=int),
        "DB_NAME": config("DB_NAME"),
        "DB_USER": config("DB_USER"),
        "DB_PASSWORD": config("DB_PASSWORD"),
        "DB_SCHEMA": config("DB_SCHEMA"),
    }
