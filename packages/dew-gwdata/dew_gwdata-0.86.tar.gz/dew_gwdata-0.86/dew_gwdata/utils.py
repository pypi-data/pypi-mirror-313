import datetime
from string import Formatter
import logging
from pathlib import Path
import os

import pandas as pd
import re
import sqlparse
import sys

from sa_gwdata import Well, Wells


def get_logger():
    from loguru import logger

    logger.remove()
    logger.add(sys.stderr, level="WARNING")
    return logger


logger = get_logger()


def get_pretty_file_size(path):
    """Return a pretty file size with GB/MB/KB/B suffix for a file."""
    stats = os.stat(path)
    kb = stats.st_size / 1024
    mb = kb / 1024
    gb = mb / 1024
    if gb > 1:
        size = f"{gb:.2f} GB"
    elif mb > 1:
        size = f"{mb:.2f} MB"
    elif kb > 1:
        size = f"{kb:.0f} KB"
    else:
        size = f"{kb * 1024:.0f} B"
    return size


def timestamp_acst(*args, tzinfo="ACST"):
    return pd.Timestamp(*args, tzinfo=datetime.timezone(datetime.timedelta(hours=9.5)))


class SQL:
    r"""Represents an SQL query or queries.

    Lower-case string template fields are filled directly with the content of the
    keyword argument, while upper-case ones are understood as iterators over a variety
    of sequence types (each then represented in the Oracle SQL correctly according to the
    sequence's element data type). E.g.

        >>> from dew_gwdata import SQL
        >>> query = SQL(
        ...     "select * from dhdb.dd_drillhole_vw where drillhole_no in {dh_no}",
        ...     dh_no=1
        ... )
        >>> for sql in query:
        ...     print(sql)
        SELECT *
        FROM dhdb.dd_drillhole_vw
        WHERE drillhole_no IN 1

    Or for a sequence data type:

    >>> from dew_gwdata import SQL
        >>> sequence_query = SQL(
        ...     "select * from dhdb.dd_drillhole_vw where drillhole_no in {DH_NO}",
        ...     dh_no=[1, 2, 3, 4, 5, 6, 7]
        ... )
        >>> for sql in sequence_query:
        ...     print(sql)
        SELECT *
        FROM dhdb.dd_drillhole_vw
        WHERE drillhole_no IN (1,2,3,4,5,6,7)

    To illustrate how a long list of qualifiers is automatically broken into the
    maximum acceptable by the database engine, let's artifically reduce the
    default of 1000 to something we can easily visualize:

        >>> sequence_query.chunksize = 3
        >>> for i, sql in enumerate(sequence_query):
        ...     print((i, sql))
        (0, 'SELECT *\nFROM dhdb.dd_drillhole_vw\nWHERE drillhole_no IN (1,2,3)')
        (1, 'SELECT *\nFROM dhdb.dd_drillhole_vw\nWHERE drillhole_no IN (4,5,6)')
        (2, 'SELECT *\nFROM dhdb.dd_drillhole_vw\nWHERE drillhole_no IN (7)')

    The kwarg to_str provides a function which turns the elements from field_list
    to a string. By default it is determined by the type of the first element.

    You can re-use a `dew_gwdata.SQL` object with a new field_list:

        >>> sequence_query_2 = SQL(sequence_query, [8, 9, 10])
        >>> for sql in sequence_query_2:
        ...     print(sql)
        SELECT *
        FROM dhdb.dd_drillhole_vw
        WHERE drillhole_no IN (8,9,10)

    """

    def __init__(
        self, sql, *args, to_str=None, chunksize=1000, ignore_fields=None, **kwargs
    ):
        if isinstance(sql, SQL):
            sql = sql.sql

        if ignore_fields is None:
            ignore_fields = ()

        self.chunksize = chunksize
        self.sql = sqlparse.format(sql, reindent=True, keyword_case="upper")

        fields = [
            fname
            for _, fname, _, _ in Formatter().parse(self.sql)
            if fname and (not fname in ignore_fields) and (not re.match(r"\d+", fname))
        ]

        # Assign a field name to each positional argument. Most of the time there
        # will only be one positional argument, and only one field in the SQL query.
        # But in general, we assign them in the order we find them, and clobber
        # anything from **kwargs in the process.

        for i in range(len(args)):
            kwargs[fields[i]] = args[i]

        # Fields in uppercase are to be filled as lists. There must only be one because
        # it's not easy to work out whether they should be joined with or, and, or whatever.
        # Fields in lowercase are to be filled as items for every query.

        uppercase_fields = [x for x in fields if x.upper() == x]
        lowercase_fields = [x for x in fields if not x in uppercase_fields]
        assert len(set(uppercase_fields)) in (0, 1)

        # logger.debug(f"uppercase_fields: {uppercase_fields}")
        # logger.debug(f"lowercase_fields: {lowercase_fields}")

        # If an SQL field e.g. DH_NO is present in kwargs in lowercase, then we need
        # to convert the kwargs to uppercase, so that everything else works sensibly.

        for upper_field in uppercase_fields:
            keys = list(kwargs.keys())
            for k in keys:
                if k == upper_field.lower():
                    kwargs[upper_field] = kwargs[k]
                    del kwargs[k]
                    break

        if len(uppercase_fields) > 0:
            items = kwargs[uppercase_fields[0]]
            if isinstance(items, Wells):
                items = getattr(
                    items, uppercase_fields[0].lower()
                )  # e.g. for {DH_NO}, fetch [w.dh_no for w in Wells]
            elif isinstance(items, pd.DataFrame):
                items = items[uppercase_fields[0].lower()].tolist()
            self.field_list = items
            self.field_list_name = uppercase_fields[0]  # remain uppercase
        else:
            self.field_list = []
            self.field_list_name = None

        # Work out the string formatting.

        self.to_str_funcs = {}
        for field_name, example in kwargs.items():
            if field_name == field_name.upper():
                if isinstance(example, pd.DataFrame):
                    example = example.iloc[0]
                else:
                    try:
                        example = example[0]
                    except IndexError:
                        example = None

            if example is None:
                # Field list is empty. We need a valid SQL query, so that we
                # return an empty table with the correct column names.
                # We assume that nothing will match an empty string in the
                # SQL where clause.

                self.to_str_funcs[field_name] = lambda x: "'{}'".format(str(x))
                self.field_list = [""]

            else:
                if isinstance(example, int):
                    self.to_str_funcs[field_name] = lambda x: str(int(x))
                elif isinstance(example, float):
                    self.to_str_funcs[field_name] = lambda x: str(float(x))
                elif (
                    isinstance(example, datetime.datetime)
                    or isinstance(example, pd.Timestamp)
                    or isinstance(example, datetime.date)
                ):
                    self.to_str_funcs[field_name] = lambda x: x.strftime(
                        "'%Y-%m-%d %H:%M:%S'"
                    )
                else:
                    self.to_str_funcs[field_name] = lambda x: "'{}'".format(str(x))

        if self.field_list_name:
            del kwargs[self.field_list_name]

        self.scalar_fields = kwargs

    def __iter__(self):
        scalar_inserts = {
            k: self.to_str_funcs[k](v) for k, v in self.scalar_fields.items()
        }

        if len(self.field_list):
            for sub_list in chunk(self.field_list, self.chunksize):
                to_str = self.to_str_funcs[self.field_list_name]
                sub_list_str = "(" + ",".join(map(to_str, sub_list)) + ")"
                inserts = dict(scalar_inserts)
                inserts[self.field_list_name] = sub_list_str
                yield self.sql.format(**inserts)
        elif len(scalar_inserts):
            yield self.sql.format(**scalar_inserts)
        else:
            yield self.sql


def chunk(l, n=1000):
    """Yield successive n-sized chunks from a list l.

    >>> from dew_gwdata.utils import chunk
    >>> for x in chunk([0, 1, 2, 3, 4], n=2):
    ...     print(x)
    [0, 1]
    [2, 3]
    [4]

    """
    y = 0
    for i in range(0, len(l), n):
        y += 1
        yield l[i : i + n]
    if y == 0:
        yield l


def apply_well_id(row, columns=("obs_no", "unit_hyphen", "dh_no")):
    for col in columns:
        if row[col]:
            return row[col]
    return ""


def cleanup_columns(df, keep_cols="well_id", drop=(), remove_metadata=False):
    """Remove unneeded drillhole identifier columns.

    Args:
        df (pandas DataFrame): dataframe to remove columns from
        keep_cols (sequence of str): columns to retain (only applies to the
            well identifiers columns; any other columns will be retained
            regardless)

    Returns: dataframe

    """
    if not "well_id" in df.columns and [
        c for c in df.columns if c in ("obs_no", "unit_hyphen", "dh_no")
    ]:
        cols = [x for x in df.columns]
        df["well_id"] = df.apply(apply_well_id, axis="columns")
        df = df[["well_id"] + cols]
    if remove_metadata:
        for col in df:
            if (
                "modified_date" in col
                or "creation_date" in col
                or "modified_by" in col
                or "created_by" in col
            ):
                df = df.drop(col, axis=1)
    keep_columns = []
    for col in df.columns:
        if (
            col
            in (
                "well_id",
                "dh_no",
                "unit_long",
                "unit_hyphen",
                "obs_no",
                "dh_name",
                "easting",
                "northing",
                "zone",
                "latitude",
                "longitude",
                "aquifer",
            )
            and not col in keep_cols
        ):
            pass
        else:
            keep_columns.append(col)
    keep_columns = [c for c in keep_columns if not c in drop]
    return df[keep_columns]


def rmdir(directory):
    """Delete a directory and all its contents without confirmation."""
    directory = Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()


def camel_to_underscore(key):
    """Convert a CamelCase string to lowercase underscore-separated.

    Example::

        >>> camel_to_underscore("InputTimeSeriesUniqueIds")
        'input_time_series_unique_ids'

    """
    chars = []
    for char in key:
        if bool(re.match("[A-Z]", char)):
            if len(chars) != 0:
                chars.append("_")
            chars.append(char.lower())
        else:
            chars.append(char)
    return "".join(chars)


def resize_image(image, width=None, height=None):
    if width == -1:
        width = None
    if height == -1:
        height = None
    if width and not height:
        return image.resize((width, int(image.height * (width / image.width))))
    elif height and not width:
        return image.resize((int(image.width * (height / image.height)), height))
    elif height and width:
        return image.resize((width, height))
    else:
        return image
