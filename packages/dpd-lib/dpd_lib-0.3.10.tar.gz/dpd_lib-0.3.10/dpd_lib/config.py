"""Simple python module for managing InfluxDB config values or 'settings'.

This module manages the four settings to properly configure the InfluxDB.
These values are pulled from environment variables that are set up prior
to the InfluxClient's use.

Typical usage example:
    import settings

    client = InfluxCLient(
        settings.influx_bucket,
        settings.influx_token,
        settings.influx_org,
        settings.influx_url
    )
"""

import os
from typing import Optional

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Class to maintain the import of InfluxDB config
    values. Values are pulled in directly via environment
    variables.

    Attributes:
        influx_bucket (str): InfluxDB Bucket to query.
        influx_token (SecretStr): InfluxDB API token.
        influx_org (str): InfluxDB organization to query.
        influx_url (str): InfluxDB url.
    """

    influx_bucket: Optional[str] = os.getenv("INFLUX_BUCKET")
    influx_url: Optional[str] = os.getenv("INFLUX_URL")
    influx_token: SecretStr = os.getenv("INFLUX_TOKEN")
    influx_org: Optional[str] = os.getenv("INFLUX_ORG")


settings = Settings()
