class InfluxNotAvailableException(Exception):
    """
    Error indicating issue contacting the InfluxDB.

    Attributes:
        STATUS_CODE: HTTP Status code
        DESCRIPTION: HTTP Error description
    """

    STATUS_CODE = 503
    DESCRIPTION = "Unable to connect to influx. Env Variables improperly set."


class BucketNotFoundException(Exception):
    """
    Error indicating the requested bucket could
    not be found.

    Attributes:
        STATUS_CODE: HTTP Status code
        DESCRIPTION: HTTP Error description
    """

    STATUS_CODE = 404
    DESCRIPTION = "Bucket Not Found."


class BadQueryException(Exception):
    """
    Error indicating a bad query.

    Attributes:
        STATUS_CODE: HTTP Status code
        DESCRIPTION: HTTP Error description
    """

    STATUS_CODE = 400
    DESCRIPTION = "Bad Query."
