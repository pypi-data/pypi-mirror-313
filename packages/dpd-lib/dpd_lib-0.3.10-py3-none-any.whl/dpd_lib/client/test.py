import asyncio
from datetime import datetime, timedelta, timezone

from dpd_lib.config import settings
from influx import InfluxClient

if __name__ == "__main__":

    client = InfluxClient(
        "dpd-test",
        settings.influx_token,
        settings.influx_org,
        settings.influx_url,
    )
    startTime: datetime = datetime.now(timezone.utc) - timedelta(hours=1)
    endTime: datetime = datetime.now(timezone.utc)

    asyncio.run(
        client.read_seismic(
            type="rsam",
            stations=["PARA"],
            t0=startTime,
            t1=endTime,
            multi_field=False,
        )
    )
    client = InfluxClient(
        "dpd-test",
        settings.influx_token,
        settings.influx_org,
        settings.influx_url,
    )
    asyncio.run(
        client.read_seismic(
            type="spectra",
            stations=["PARA"],
            t0=startTime,
            t1=endTime,
            multi_field=True,
            plot_results=True,
        )
    )
