from collections import OrderedDict
from io import BytesIO
from typing import Dict, List

import matplotlib as m
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from dateutil import tz
from dpd_lib.models import InfluxRecord
from dpd_lib.utils import grab_obspy_stream
from loguru import logger
from matplotlib.colors import LinearSegmentedColormap
from obspy import Stream, UTCDateTime

np.random.seed(1)


def plot_spectrogram(station: str, records: List[InfluxRecord]):
    """
    Function to generate a plotly spectrogram from Influx Data.

    Arguments:
        station (str): FDSN Station
        records (List[InfluxRecord]): List of InfluxRecords to plot.

    Returns:
        HTML Plotly Plot
    """
    x = [
        (record.timestamp).astimezone(tz.gettz("US/Pacific"))
        for record in records
    ]
    y = list(set([key for record in records for key in record.field_keys]))

    yzDict = OrderedDict[float, List]({y: [] for y in y})

    for record in records:
        for i in range(len(record.field_keys)):
            yzDict[record.field_keys[i]].append(record.field_values[i])

    fig = go.Figure(
        data=go.Heatmap(
            z=list(yzDict.values()),
            x=x,
            y=list(yzDict.keys()),
            colorscale="Viridis",
        )
    )

    fig.update_layout(title=f"{station} Spectrogram")

    fig = pio.to_html(fig, full_html=True)

    return fig


def plot_spectogram_raw(
    riverDist: Dict[str, float],
    t0: UTCDateTime,
    t1: UTCDateTime,
    type: str = "seismic",
) -> BytesIO:
    """
    Function to generate a Matplotlib spectrogram using raw obspy data.
    Single image is created with stacked plots for multiple stations.

    Arguments:
        riverDist (Dict[str, str]): Dictionary of fdsn codes + riverDist
        t0 (UTCDateTime): Plot start time
        t1 (UTCDateTime): Plot end time

    Returns:
        BytesIO: Image Buffer
    """
    m.use("Agg")

    plot_duration = 600  # 10 min

    # grab data #
    st = Stream()

    # Sort FDSN by riverDist
    riverDist = dict(sorted(riverDist.items(), key=lambda item: item[1]))
    for station in riverDist.keys():
        stream_tr = grab_obspy_stream([station], t0, t1, "localhost", "16022")
        if len(stream_tr) > 0:
            st += stream_tr[0]
        else:
            logger.warning(f"No Data: Station {station}.")
            continue

    # preprocess data #
    st.detrend("demean")
    [
        tr.decimate(2, no_filter=True)
        for tr in st
        if tr.stats.sampling_rate == 100
    ]
    [
        tr.decimate(2, no_filter=True)
        for tr in st
        if tr.stats.sampling_rate == 50
    ]

    colors = cm.jet(np.linspace(-1, 1.2, 256))
    color_map = LinearSegmentedColormap.from_list("Upper Half", colors)
    plt.figure(figsize=(4.5, 4.5))
    for i, tr in enumerate(st):
        ax = plt.subplot(len(st), 1, i + 1)
        tr.spectrogram(
            title="",
            log=False,
            samp_rate=tr.stats.sampling_rate,
            dbscale=True,
            per_lap=0.859375,
            wlen=2.56,
            cmap=color_map,
            axes=ax,
        )
        ax.set_yticks([3, 6, 9, 12])
        ax.set_ylabel(
            "Hz",
            fontsize=7,
            rotation="horizontal",
            multialignment="center",
            horizontalalignment="right",
            verticalalignment="center",
        )
        ax.yaxis.set_ticks_position("left")
        ax.tick_params("y", labelsize=4)
        ax.set_title(
            f"{tr.stats.station}.{tr.stats.channel}",
            fontsize=7,
            verticalalignment="center",
        )
        if i < len(st) - 1:
            ax.set_xticks([])
        else:
            seis_tick_fmt = "%H:%M"
            if plot_duration in [1800, 3600, 5400, 7200]:
                n_seis_ticks = 7
            elif plot_duration in [
                300,
                600,
                900,
                1200,
                1500,
                2100,
                2400,
                2700,
                3000,
                3300,
            ]:
                n_seis_ticks = 6
            else:
                n_seis_ticks = 6
                seis_tick_fmt = "%H:%M:%S"
            d_sec = np.linspace(0, t1 - t0, n_seis_ticks)
            ax.set_xticks(d_sec)
            T = [tr.stats.starttime + dt for dt in d_sec]
            ax.set_xticklabels([t.strftime(seis_tick_fmt) for t in T])
            ax.tick_params("x", labelsize=5)
            ax.set_xlabel(tr.stats.starttime.strftime("%Y-%m-%d") + " UTC")

    plt.subplots_adjust(
        left=0.08, right=0.94, top=0.92, bottom=0.1, hspace=0.1
    )
    plt.tight_layout(pad=0.5)
    buffer = BytesIO()
    plt.savefig(buffer, format="png")

    buffer.seek(0)

    return buffer
