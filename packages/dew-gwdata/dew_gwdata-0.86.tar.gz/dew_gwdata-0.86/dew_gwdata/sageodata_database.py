import sageodata_db


def connect(user="gwquery", password="gwquery", **kwargs):
    """Connect to SA Geodata.

    Args:
        user (str): oracle user
        password (str): password
        service_name (str): version of SA Geodata you would like to connect
            to - options are "DMED.WORLD" or "dev"; "DMET.WORLD" or "test" or
            "QA"; or "DMEP.WORLD" or "prod" - see
            :func:`sageodata_db.config.normalize_service_name` for details.

    Other keyword arguments are passed to
    :func:`sageodata_db.config.make_connection_string`.

    Returns: a :class:`sageodata_db.SAGeodataConnection` object.

    Example:

        >>> from dew_gwdata import sageodata
        >>> db = sageodata()
        >>> db
        <sageodata_db.connection.SAGeodataConnection to gwquery@pirsapd07.pirsa.sa.gov.au:1521/DMEP.World>

    """
    db = sageodata_db.connect(user=user, password=password, **kwargs)
    return db
