# Derived Project Database Library

## Overview

This libary contains several functions that enable the processing, storage, and retrieve of seismic and infrasound signal data. The underlying storage mechanism that sits under each respective component is an [InfluxDB](https://docs.influxdata.com/influxdb/v2/) database that we call the Derived Product Database (DPD).

The DPD is a time-series storage system that contains *processed* seismic and infrasound signal data. In theory, the DPD can be extended to store *any* time series data and the `dpd_lib` can be used to upload and retrieve that data assuming the underlying system has been set up correctly.

### The DPD Library

The DPD Library is a python library comprised of a number of functions that enable users to upload and retrieve signal data stored in an underlying DPD. The functions typically follow the following format:

* `read_[signal_type]()`
* `record_[signal_type]()`
* `list_[signal_type]()`

So, for example, to retrieve infrasound data, one would import and use `read_infrasound()` with the proper arguments. Just like with the DPD Agent, the DPD Library depends on four InfluxDB environment variables to run.

The library can be found at [pypi.org](https://pypi.org/project/dpd-lib/) and installed using pip.