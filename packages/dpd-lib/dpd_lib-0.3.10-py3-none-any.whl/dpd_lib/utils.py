import os
import re
from datetime import datetime, timedelta, timezone
from typing import List, Optional

import numpy as np
from loguru import logger
from obspy import Stream, Trace
from obspy.clients.earthworm import Client
from obspy.clients.fdsn import Client as Client_IRIS
from obspy.core import UTCDateTime
from obspy.core.inventory import Inventory, read_inventory


def normalize_str(stream: Stream, scalar: float = 1.0) -> Stream:
    """
    Function to normalize a stream by the maximum value in each trace.

    Arguments:
        stream (Stream): Obspy Stream
        scalar: (float): Scalar to multiply stream for visualization

    Returns:
        Stream: Normalized Stream
    """
    for tr in stream:
        max_value = np.max(
            np.abs(tr.data)
        )  # Find the maximum absolute value of the trace

        if max_value > 0:
            tr.data /= max_value  # Normalize the trace by its maximum value

        tr.data *= scalar  # Scale

    return stream


def moving_average_trace(trace: Trace, window_duration: int = 1) -> Trace:
    """
    Function to calculate the moving average of an obspy stream.

    Arguments:
        trace (Trace): Obspy trace
        window_duration (int): Window size of moving average (default 1s)

    Returns:
        Trace: Updated trace
    """
    # Extract the trace data and sampling rate
    data = trace.data
    sampling_rate = trace.stats.sampling_rate

    # Calculate the window size in terms of samples
    window_size = int(window_duration * sampling_rate)

    # Compute the moving average using numpy's convolution
    window = np.ones(window_size) / window_size
    moving_avg_data = np.convolve(data, window, mode="same")

    # Replace the data in the trace with the moving average result
    trace.data = moving_avg_data
    logger.info(trace.stats.sampling_rate)
    trace.decimate(factor=int(trace.stats.sampling_rate), no_filter=True)

    return trace


def moving_average_stream(stream: Stream, window_duration: int = 1) -> Stream:
    """
    Function to calculate moving average for Stream

    Arguments:
        stream (Stream): Obspy Stream
        window_duration (int): Window size of moving average (default 1s)

    Returns:
        Stream: Updated Stream
    """
    # Apply moving average for each trace in the stream
    for trace in stream:
        moving_average_trace(trace, window_duration)

    return stream


def get_digital_count(
    network: str,
    station: str,
    location: str,
    channel: str,
    metadata_filepath: Optional[str],
) -> float:
    """
    Function to retrieve sensitivity or digital count from
    station metdata.

    Arguments:
        network (str): FDSN Network
        station (str): FDSN Station
        location (str): FDSN Location
        channel (str): FDSN Channel
        metadata_filepath (str): Filepath to metadata folder

    Returns:
        float: Station sensitivity
    """
    if location == "--":
        location = ""
    metadata = get_metadata(
        network=network,
        station=station,
        metadata_filepath=metadata_filepath,
    )
    count = 1.0

    fdsn = f"{network}.{station}.{location}.{channel}"

    if fdsn not in str(metadata):
        logger.info(f"{fdsn} not present in station metadata.")
        logger.info("Attempting to retrieve similar fdsn code.")

        seismic_pattern = r".*HZ$"
        infrasound_pattern = r".*DF$"
        if bool(re.match(seismic_pattern, channel)):
            pattern = r"\b[A-Z]{2}\.[A-Z0-9]+\.[A-Z0-9]*\.(?:B|C|E|H)HZ\b"
            matches = re.findall(pattern, str(metadata))
            fdsn = matches[0] if matches else fdsn
        if bool(re.match(infrasound_pattern, channel)):
            pattern = r"\b[A-Z]{2}\.[A-Z0-9]+\.[A-Z0-9]*\.(?:B|C|E|H)DF\b"
            matches = re.findall(pattern, str(metadata))
            fdsn = matches[0] if matches else fdsn

    count = metadata.get_response(
        fdsn, UTCDateTime.utcnow()
    ).instrument_sensitivity.value

    return count


def get_metadata(
    network: str, station: str, metadata_filepath: Optional[str]
) -> Inventory:
    """
    Returns metadata for a given station.
    If a local XML file is present, load into inventory.
    If no local XML file is present, query IRIS and save XML file.

    Arguments:
        network (str): FDSN Network Code
        station (str): FDSN Station Code
        metadata_filepath (str): Filepath to metadata folder

    Returns:
        Inventory: Metadata of station
    """
    metadata = None
    station_filename = f"{metadata_filepath}/{network}.{station}-metadata.xml"

    metadata_present = os.path.isfile(station_filename)

    out_of_date = False

    if metadata_present:
        logger.debug(f"STATION METADATA FILE FOUND: {station_filename}.")
        metadata = read_inventory(
            path_or_file_object=f"{station_filename}",
        )
        out_of_date = (
            datetime.now(timezone.utc).timestamp()
            - metadata.created.datetime.timestamp()
            > timedelta(days=7).total_seconds()
        )
        logger.debug(f"STATION METADATA FILE IS OUT-OF-DATE: {out_of_date}.")

    if not metadata_present or out_of_date:
        logger.debug(f"FILE NOT FOUND OR OUT-OF-DATE: {station_filename}.")
        iclient = Client_IRIS("IRIS")
        try:
            metadata = iclient.get_stations(
                network=network,
                station=station,
                level="response",
                starttime=UTCDateTime() - 600,
                endtime=UTCDateTime() - 550,
            )
            metadata.write(
                path_or_file_object=station_filename, format="STATIONXML"
            )
        except Exception as e:
            logger.warning(f"STATION ({station}) NOT AVAILABLE. Error: {e}")
    return metadata


def grab_obspy_stream(
    fdsn: List[str],
    t0: UTCDateTime,
    t1: UTCDateTime,
    hostname: str,
    port: str,
) -> Stream:
    """
    Returns stream for a given station.
    Converts stream data to earth units using station's dcount
    and converts to seismic traces to micro m/s

    Arguments:
        fdsn: List[str] list of fdsn network codes.
        t0 (datetime): The timestamp of the beginning of time window.
        t1 (datetime): The timestamp of the end of the time window.
        host (str): The host - Iris or local earthworm
        port (int): Port of local IRIS host

    Returns:
        Stream: Station Obspy Stream
    """
    stream = Stream()
    for station_code in fdsn:
        network, station, location, channel = station_code.split(".")
        stream_st = Stream()
        if hostname == "IRIS":
            client = Client_IRIS("IRIS")
            stream_st = client.get_waveforms(
                network,
                station,
                location,
                channel,
                t0,
                t1,
            )
        else:
            client = Client(hostname, int(port))
            stream_st = client.get_waveforms(
                network,
                station,
                location,
                channel,
                t0,
                t1,
                cleanup=True,
            )

        if len(stream_st) == 0:
            logger.error(f"No Data: Station {station} Channel {channel}.")
            stream_tr = Trace()
            continue

        stream_tr = stream_st[0]

        sampling_rate = stream_tr.stats.sampling_rate
        stream_tr.data = stream_tr.data[: int((t1 - t0) * sampling_rate)]

        seismic_pattern = r".*HZ$"
        infrasound_pattern = r".*DF$"

        if bool(re.match(seismic_pattern, channel)):
            dcount = get_digital_count(
                network,
                station,
                location,
                channel,
                os.getenv("STATION_METADATA_DIR"),
            )
            # Divide by dcount and convert to µm/s
            # for trace in stream_tr:
            stream_tr.data = (stream_tr.data / dcount) * 10e6
        elif bool(re.match(infrasound_pattern, channel)):
            channel = "BDF"
            location = "01"
            dcount = get_digital_count(
                network,
                station,
                location,
                channel,
                os.getenv("STATION_METADATA_DIR"),
            )
            # Only divide by dcount
            stream_tr.data = (stream_tr.data / dcount) * 10e6
        else:
            logger.error("Unknown Channel Code.")

        stream += stream_tr

    return stream
