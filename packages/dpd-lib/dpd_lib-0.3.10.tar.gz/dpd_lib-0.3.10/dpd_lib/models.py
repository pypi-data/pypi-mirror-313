from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field


class InfluxRecord(BaseModel):
    """
    A pydantic model to structure influx records stored
    in the InfluxDB.

    Attributes:
        type (str): Type of metric.
        station (str): Station metric was originally recorded.
        drainage (str): Drainage where station is located
        riverDist (str): Distance along drainage
        timestamp (datetime): Center of time window of processed metric.
        field_keys (List[Any]): List of record field keys
        field_values (List[float]): List of record field values
    """

    type: str = Field(description="Type of infrasound record")
    station: str = Field(description="Station associated with record")
    drainage: str = Field(description="Drainage station located in")
    riverDist: str = Field(description="Distance along drainage (KM)")
    volcano: str = Field(description="Station Volcano")
    timestamp: datetime = Field(description="record timestamp")
    field_keys: List[Any] = Field(description="list of fields")
    field_values: List[float] = Field(description="list of values")


class InfluxAlertRecord(BaseModel):
    """
    A pydantic model to structure influx alert records stored
    in the InfluxDB.

    Attributes:
        type (str): Type of metric.
        drainage (str): Drainage where station is located
        timestamp (datetime): Center of time window of processed metric.
    """

    type: str = Field(description="Type of infrasound record")
    drainage: str = Field(description="Drainage station located in")
    timestamp: datetime = Field(description="record timestamp")
    value: float = Field(description="value of record")


class JsonRecord(BaseModel):
    """
    A pydantic model to structure Json records returned by
    obspy.

    Attributes:
        type (str): Type of metric.
        station (str): Station metric was originally recorded.
        drainage (str): Drainage where station is located
        riverDist (str): Distance along drainage
        timestamp (datetime): Center of time window of processed metric.
        field_keys (List[Any]): List of record field keys
        field_values (List[float]): List of record field values
    """

    network: str = Field(description="FDSN Network")
    station: str = Field(description="FDSN Station")
    channel: str = Field(description="FDSN Channel")
    location: str = Field(description="FDSN Location")
    timestamp: datetime = Field(description="record timestamp")
    value: float = Field(description="Value of record")


class InfluxQueryObject(BaseModel):
    """
    A pydantic model to structure influx records stored
    in the InfluxDB.

    Attributes:
        records (List[InfluxRecord]): List of influx records
        plot (Optional[str]): Influx plot
    """

    records: List[BaseModel] = Field(description="List of influx records")
    plot: Optional[str] = Field(description="Base64 encoded plot of records")
