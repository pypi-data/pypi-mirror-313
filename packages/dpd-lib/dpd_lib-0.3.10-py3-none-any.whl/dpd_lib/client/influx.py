"""Primary python module for interacting with signal data in the DPD.

This module contains the InfluxClient and it's primary functions.
These functions allow a user to interact with an underlying DPD (InfluxDB)
to read and upload signal data. This module relies on four Influx env
variables to query the correct system.

Typical usage example:

  client = InfluxCLient(
    INFLUX_BUCKET,
    INFLUX_TOKEN,
    INFLUX_ORG,
    INFLUX_URL
  )
  data = client.record_infrasound(
    type,
    value,
    station,
    timestamp
  )
"""

import json
import re
from collections import OrderedDict
from datetime import datetime, timedelta, timezone
from typing import Any, List, Optional

from dpd_lib.client.exceptions import (
    BadQueryException,
    BucketNotFoundException,
    InfluxNotAvailableException,
)
from dpd_lib.models import InfluxAlertRecord, InfluxQueryObject, InfluxRecord
from dpd_lib.plot import plot_spectrogram
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.rest import ApiException
from loguru import logger
from pydantic import SecretStr
from urllib3.exceptions import NewConnectionError

INFRASOUND_TYPES = [
    "",
    "mdccm",
    "velocity",
    "riam",
    "pressure",
    "azimuth",
    "envelope",
    "spectra",
]
SEISMIC_TYPES = ["", "rsam", "envelope", "spectra"]
ALERT_TYPES = [
    "",
    "Alarm",
    "Seismic-Trigger",
    "Infrasound-Trigger",
    "RSAM-Element",
    "Velocity-Element",
    "Pressure-Element",
    "Azimuth-Element",
]


class InfluxClient:
    """
    A restricted client which implements an interface
    to query data from the influx database.

    Attributes:
        bucket (str): InfluxDB Bucket to query.
        _client (InfluxDBClient): The instantiated
            InfluxDB client.
    """

    def __init__(
        self,
        bucket: Optional[str],
        token: SecretStr,
        org: Optional[str],
        url: Optional[str],
    ) -> None:
        """
        Initializes the InfluxDB Client based-off bucket, org, and url.
        Also requires an API token.

        Args:
            bucket (str): InfluxDB Bucket to query.
            token (SecretStr): InfluxDB API token.
            org (str): InfluxDB organization to query.
            url (str): InfluxDB url.
        """
        self.bucket = bucket

        try:

            if any(
                not env or len(env) == 0 for env in [bucket, token, org, url]
            ):
                raise InfluxNotAvailableException(
                    "One or more $INFLUX_ Variables not set."
                )
            else:
                self._client = InfluxDBClient(
                    url=url, token=token.get_secret_value(), org=org
                )
        except Exception as e:
            raise InfluxNotAvailableException(str(e))

    async def record_seismic(
        self,
        type: str,
        station: str,
        drainage: str,
        riverDist: str,
        volcano: str,
        timestamp: datetime,
        field_keys: List[Any],
        field_values: List[Any],
    ) -> None:
        """
        Records new seismic record for a given timestamp

        Arguments:
            type (str): The type of seismic record
            station (str): The associated station
            drainage (str): Drainage where station located
            riverDist (str): Distance along drainage (KM)
            timestamp (datetime): The timestamp
            field_keys: (List[Any]): The keys (names) of various fields
            field_values: (List[Any]): The values of the various fields

        Returns:
            None

        Raises:
            InfluxNotAvailableException: An error occurred
                while contacting the InfluxDB.
            BadQueryException: There is an issue with the
                influx query.
            BucketNotFoundException: The requested bucket
            is not present in the DB.
        """
        if type not in SEISMIC_TYPES:
            raise BadQueryException(
                f"Seismic type not accepted. Accepted types: {SEISMIC_TYPES}."
            )
        p = {
            "measurement": type,
            "tags": {
                "station": station,
                "drainage": drainage,
                "riverDist": riverDist,
                "volcano": volcano,
            },
            "fields": None,
            "time": timestamp,
        }
        field_dictionary = {}
        for field_key, field_value in zip(field_keys, field_values):
            field_dictionary[field_key] = field_value

        p["fields"] = field_dictionary

        point = Point.from_dict(p)

        await self._insert([point])

    async def read_seismic(
        self,
        type: str = "",
        stations: List[str] = [],
        t0: datetime = datetime.now(timezone.utc) - timedelta(seconds=15),
        t1: datetime = datetime.now(timezone.utc),
        multi_field: bool = False,
        plot_results: bool = False,
    ) -> InfluxQueryObject:
        """
        Reads seismic records for a given type, station list, and timestamp

        Arguments:
            type (str): The type of seismic record
            station (List(str)): The station of seismic record
            t0 (datetime): the beginning of the timerange
            t1 (datetime): The end of the timerange
            multi_field (bool): Whether record has multiple fields
            plot_results (bool): Whether to return plotted results

        Returns:
            InfluxQueryObject: All records of a
            certain type for a given range.

        Raises:
            InfluxNotAvailableException: An error occurred
                while contacting the InfluxDB.
            BadQueryException: There is an issue with the
                influx query.
            BucketNotFoundException: The requested bucket
            is not present in the DB.
        """
        if type not in SEISMIC_TYPES:
            raise BadQueryException(
                f"Seismic type not accepted. Accepted types: {SEISMIC_TYPES}."
            )
        query = """from(bucket:"{0}")
        |> range(start: {1}, stop: {2})""".format(
            self.bucket,
            t0.strftime("%Y-%m-%dT%H:%M:%SZ"),
            t1.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        if type != "":
            query += '|> filter(fn:(r) => r._measurement == "{0}")'.format(
                type
            )
        if len(stations) != 0:
            query += """
            |> filter(fn:(r) => contains(value: r.station, set: {0}))
            """.format(
                json.dumps(stations)
            )
        if multi_field:
            query += """
            |> pivot(
                rowKey: ["_time"],
                columnKey: ["_field"],
                valueColumn: "_value")"""
        records = await self._query(query)
        plot = (
            self.plot_seismic(type=type, station=stations[0], records=records)
            if plot_results
            else None
        )

        return InfluxQueryObject(records=records, plot=plot)

    def plot_seismic(
        self, type: str, station: str, records: List[InfluxRecord]
    ):
        """
        Plots seismic records for a given type, station list, and timestamp

        Arguments:
            records (List[InfluxRecord]): List of influx records to plot

        Returns:
            [TODO]

        Raises:
            InfluxNotAvailableException: An error occurred
                while contacting the InfluxDB.
            BadQueryException: There is an issue with the
                influx query.
            BucketNotFoundException: The requested bucket
            is not present in the DB.
        """

        plot = None
        if type == "spectra":
            plot = plot_spectrogram(station=station, records=records)
        else:
            logger.info("Not accepted type")

        return plot

    async def record_infrasound(
        self,
        type: str,
        station: str,
        drainage: str,
        riverDist: str,
        volcano: str,
        timestamp: datetime,
        field_keys: List[Any],
        field_values: List[Any],
    ) -> None:
        """
        Records new infrasound record for a given timestamp

        Arguments:
            type (str): The type of infrasound record
            station (str): The associated station
            drainage (str): Drainage where station located
            riverDist (str): Distance along drainage (KM)
            timestamp (datetime): The timestamp
            field_keys: (List[Any]): The keys (names) of various fields
            field_values: (List[Any]): The values of the various fields

        Returns:
            None

        Raises:
            InfluxNotAvailableException: An error occurred
                while contacting the InfluxDB.
            BadQueryException: There is an issue with the
                influx query.
            BucketNotFoundException: The requested bucket
            is not present in the DB.
        """

        if type not in INFRASOUND_TYPES:
            raise BadQueryException(
                f"Type not accepted. Accepted types: {INFRASOUND_TYPES}."
            )
        p = {
            "measurement": type,
            "tags": {
                "station": station,
                "drainage": drainage,
                "riverDist": riverDist,
                "volcano": volcano,
            },
            "fields": {},
            "time": timestamp,
        }
        field_dictionary = {}
        for field_key, field_value in zip(field_keys, field_values):
            field_dictionary[field_key] = field_value

        p["fields"] = field_dictionary

        point = Point.from_dict(p)

        await self._insert([point])

    async def read_infrasound(
        self,
        type: str = "",
        stations: List[str] = [],
        t0: datetime = datetime.now(timezone.utc) - timedelta(seconds=15),
        t1: datetime = datetime.now(timezone.utc),
        multi_field: bool = False,
        plot_results: bool = False,
    ) -> InfluxQueryObject:
        """
        Reads infrasound records for a given type, station list, and timestamp

        Arguments:
            type (str): The type of infrasound record
            station (List(str)): The station of infrasound record
            t0 (datetime): the beginning of the timerange
            t1 (datetime): The end of the timerange
            multi_field (bool): Whether record has multiple fields
            plot_results (bool): Whether to return plotted results

        Returns:
            InfluxQueryObject: All records of a
            certain type for a given range.

        Raises:
            InfluxNotAvailableException: An error occurred
                while contacting the InfluxDB.
            BadQueryException: There is an issue with the
                influx query.
            BucketNotFoundException: The requested bucket
            is not present in the DB.
        """
        if type not in INFRASOUND_TYPES:
            raise BadQueryException(
                f"Type not accepted. Accepted types: {INFRASOUND_TYPES}."
            )
        query = """from(bucket:"{0}")
        |> range(start: {1}, stop: {2})""".format(
            self.bucket,
            t0.strftime("%Y-%m-%dT%H:%M:%SZ"),
            t1.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        if type != "":
            query += '|> filter(fn:(r) => r._measurement == "{0}")'.format(
                type
            )
        if len(stations) != 0:
            query += """
            |> filter(fn:(r) => contains(value: r.station, set: {0}))
            """.format(
                json.dumps(stations)
            )
        if multi_field:
            query += """
            |> pivot(
                rowKey: ["_time"],
                columnKey: ["_field"],
                valueColumn: "_value")"""
        records = await self._query(query)
        plot = (
            self.plot_seismic(type=type, station=stations[0], records=records)
            if plot_results
            else None
        )
        return InfluxQueryObject(records=records, plot=plot)

    def plot_infrasound(
        self, type: str, station: str, records: List[InfluxRecord]
    ):
        """
        Plots seismic records for a given type, station list, and timestamp

        Arguments:
            records (List[InfluxRecord]): List of influx records to plot

        Returns:
            [TODO]

        Raises:
            InfluxNotAvailableException: An error occurred
                while contacting the InfluxDB.
            BadQueryException: There is an issue with the
                influx query.
            BucketNotFoundException: The requested bucket
            is not present in the DB.
        """

        plot = None
        if type == "spectra":
            plot = plot_spectrogram(station=station, records=records)
        else:
            logger.info("Not accepted type")

        return plot

    async def list_records(
        self,
        t0: datetime = datetime.now(timezone.utc) - timedelta(seconds=15),
        t1: datetime = datetime.now(timezone.utc),
    ) -> InfluxQueryObject:
        """
        Lists all records for given time range.

        Arguments:
            t0 (datetime): the beginning of the timerange
            t1 (datetime): The end of the timerange

        Returns:
            InfluxQueryObject:
                All records for given time range.

        Raises:
            InfluxNotAvailableException: An error occurred
                while contacting the InfluxDB.
            BadQueryException: There is an issue with the
                influx query.
            BucketNotFoundException: The requested bucket
            is not present in the DB.
        """
        query = """from(bucket:"{0}")
        |> range(start: {1}, stop: {2})""".format(
            self.bucket,
            t0.strftime("%Y-%m-%dT%H:%M:%SZ"),
            t1.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        return await InfluxQueryObject(records=self._query(query))

    async def _insert(self, p_arr: List[Point]) -> Any:
        """
        Inserts an array of points into the database via InfluxDB write_api

        Arguments:
            p (Point): The data point to insert into the database

        Returns:
            Any: Results from the write_api

        Raises:
            InfluxNotAvailableException: An error occurred
                while contacting the InfluxDB.
            BadQueryException: There is an issue with the
                influx query.
            BucketNotFoundException: The requested bucket
            is not present in the DB.
        """
        write_api = self._client.write_api(write_options=SYNCHRONOUS)
        try:
            res = write_api.write(bucket=self.bucket, record=p_arr)
        except NewConnectionError:
            raise InfluxNotAvailableException()
        except ApiException as e:
            if e.status and e.status == 400:
                raise BadQueryException()
            if e.status and e.status == 404:
                raise BucketNotFoundException()
            raise InfluxNotAvailableException()
        logger.info(f"{res=}")
        return res

    async def _query(self, query: str = "") -> List[InfluxRecord]:
        """
        Queries the InfluxDB with the proivded query string

        Arguments:
            query (str): The raw query string to pass to InfluxDB
            multi_field (bool): Whether the expected records have
                multiple fields.

        Returns:
            List[InfluxRecord]:
                A list of records that match the query

        Raises:
            InfluxNotAvailableException: An error occurred
                while contacting the InfluxDB.
            BadQueryException: There is an issue with the
                influx query.
            BucketNotFoundException: The requested bucket
            is not present in the DB.
        """
        logger.debug(f"Running {query=}")
        query_api = self._client.query_api()
        try:
            result = query_api.query(query=query)
        except NewConnectionError:
            raise InfluxNotAvailableException()
        except ApiException as e:
            if e.status and e.status == 400:
                raise BadQueryException()
            if e.status and e.status == 404:
                raise BucketNotFoundException()
            raise InfluxNotAvailableException()
        res = []
        for table in result:
            for record in table.records:
                fieldKV = {
                    i: record.values[i]
                    for i in record.values
                    if type(record.values[i]) is float
                }
                if all(
                    [
                        re.match(r"^-?\d+(?:\.\d+)$", key) is not None
                        for key in fieldKV.keys()
                    ]
                ):
                    fieldKV = OrderedDict(
                        sorted(
                            {float(k): v for k, v in fieldKV.items()}.items()
                        )
                    )
                else:
                    fieldKV = {record.get_field(): record.get_value()}

                r = InfluxRecord(
                    type=record.get_measurement(),
                    station=record.values.get("station"),
                    drainage=record.values.get("drainage"),
                    riverDist=record.values.get("riverDist"),
                    timestamp=record.get_time(),
                    field_keys=fieldKV.keys(),
                    field_values=fieldKV.values(),
                )
                res.append(r)
        logger.debug(f"Query returned {len(res)} records.")
        return res

    async def read_alert(
        self,
        bucket,
        type: str = "Alarm",
        drainage: str = "",
        last: bool = False,
        t0: datetime = datetime.now(timezone.utc) - timedelta(minutes=5),
        t1: datetime = datetime.now(timezone.utc),
    ) -> InfluxQueryObject:
        """
        NOTE: HOW can I accept 'tags' as opposed to specific tags
        Would significantly generalize. Could apply to other endpoints.

        Reads alert records for a given alert type in given drainage

        Arguments:
            type (str): The type of alert record
            drainage (str): The drainage of alert record
            last (bool): Whether to grab max or latest value for period.
            window (int): Length of time to look for alerts
            t0 (datetime): the beginning of the timerange
            t1 (datetime): The end of the timerange

        Returns:
            InfluxQueryObject: All records of a
            certain type for a given range.

        Raises:
            InfluxNotAvailableException: An error occurred
                while contacting the InfluxDB.
            BadQueryException: There is an issue with the
                influx query.
            BucketNotFoundException: The requested bucket
            is not present in the DB.
        """
        if type not in ALERT_TYPES:
            raise BadQueryException(
                f"Seismic type not accepted. Accepted types: {ALERT_TYPES}."
            )
        query = """from(bucket:"{0}")
            |> range(start: {1}, stop: {2})""".format(
            bucket,
            t0.strftime("%Y-%m-%dT%H:%M:%SZ"),
            t1.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        if type != "":
            query += '|> filter(fn:(r) => r._measurement == "{0}")'.format(
                type
            )
        if drainage != "":
            query += '|> filter(fn: (r) => r.drainage == "{0}")'.format(
                drainage
            )

        # TODO Remove test tag
        query += '|> filter(fn: (r) => r.mode == "TEST")'

        # Grab max() for period
        if last:
            query += "|> last()"
        else:
            query += "|> max()"

        logger.debug(f"Running {query=}")

        query_api = self._client.query_api()

        try:
            result = query_api.query(query=query)
        except NewConnectionError:
            raise InfluxNotAvailableException()
        except ApiException as e:
            if e.status and e.status == 400:
                raise BadQueryException()
            if e.status and e.status == 404:
                raise BucketNotFoundException()
            raise InfluxNotAvailableException()
        res = []
        for table in result:
            for record in table.records:
                r = InfluxAlertRecord(
                    type=record.get_measurement(),
                    drainage=record.values.get("drainage"),
                    timestamp=record.get_time(),
                    value=record.get_value(),
                )
                res.append(r)

        return InfluxQueryObject(records=res, plot=None)
