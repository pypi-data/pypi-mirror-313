import pyodbc

__all__ = ["get_wde_connection"]


def get_wde_connection():
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=sql2012-prod.env.sa.gov.au;"
        "Database=WDE_Extended;"
        "Trusted_Connection=yes;"
    )
    return conn


class WDEDatabase:
    def __init__(self, *args, **kwargs):
        self.conn = get_wde_connection(*args, **kwargs)

    # add a method to run the predefined queries.
