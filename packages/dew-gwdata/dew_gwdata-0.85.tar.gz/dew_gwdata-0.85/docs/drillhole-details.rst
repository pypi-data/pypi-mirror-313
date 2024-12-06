Drillhole details
====================

Identifying drillholes
----------------------

The fundamental identifer for drillholes in ``dew_gwdata`` is the drillhole number. It's an integer which
uniquely identifies each drillhole. You can obtain these for any combination of well identifiers using
:meth:`sageodata_db.SAGeodataConnection.find_wells`:

.. code-block:: python

    >>> import dew_gwdata as gd
    >>> con = gd.connect_to_sageodata()
    >>> type(con)
    <class 'sageodata_db.connection.SAGeodataConnection'>

This can be used to identify wells:

.. code-block:: python

    >>> dhs = con.find_wells("CAR011,  KON 33 ")
    >>> type(dhs)
    <class 'sa_gwdata.identifiers.Wells'>
    >>> print(dhs)
    ['CAR011', 'KON033']

You can convert these result objects to a ``pandas.DataFrame``:

.. code-block:: python

    >>> df = dhs.df()
    >>> print(df.info())
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 2 entries, 0 to 1
    Data columns (total 25 columns):
    #   Column            Non-Null Count  Dtype  
    ---  ------            --------------  -----  
    0   dh_no             2 non-null      int64  
    1   id                2 non-null      object 
    2   title             2 non-null      object 
    3   name              2 non-null      object 
    4   unit_no.map       2 non-null      int64  
    5   unit_no.seq       2 non-null      int64  
    6   unit_no.hyphen    2 non-null      object 
    7   unit_no.long      2 non-null      object 
    8   unit_no.long_int  2 non-null      int64  
    9   unit_no.wilma     2 non-null      object 
    10  unit_no.hydstra   2 non-null      object 
    11  obs_no.plan       2 non-null      object 
    12  obs_no.seq        2 non-null      int64  
    13  obs_no.id         2 non-null      object 
    14  obs_no.egis       2 non-null      object 
    15  well_id           2 non-null      object 
    16  dh_name           2 non-null      object 
    17  easting           2 non-null      float64
    18  northing          2 non-null      float64
    19  zone              2 non-null      int64  
    20  latitude          2 non-null      float64
    21  longitude         2 non-null      float64
    22  aquifer           2 non-null      object 
    23  pwa               2 non-null      object 
    24  pwra              0 non-null      object 
    dtypes: float64(4), int64(6), object(15)
    memory usage: 528.0+ bytes
    None

An example of the type of data in each field:

.. code-block:: python

    >>> print(df.iloc[0])
    dh_no                                                 105113
    id                                                    CAR011
    title                            7021-1058 / CAR011 / CAR 11
    name                                                  CAR 11
    unit_no.map                                             7021
    unit_no.seq                                             1058
    unit_no.hyphen                                     7021-1058
    unit_no.long                                       702101058
    unit_no.long_int                                   702101058
    unit_no.wilma                                     7021-01058
    unit_no.hydstra                                   G702101058
    obs_no.plan                                              CAR
    obs_no.seq                                                11
    obs_no.id                                             CAR011
    obs_no.egis                                           CAR 11
    well_id                                               CAR011
    dh_name                                               CAR 11
    easting                                            495281.78
    northing                                          5788906.35
    zone                                                      54
    latitude                                          -38.047563
    longitude                                         140.946225
    aquifer             Thgc+Thgr(U1)+Thgr(U2)+Thgr(U3)+Thgr(U4)
    pwa                                    Lower Limestone Coast
    pwra                                                    None
    Name: 0, dtype: object

Replacement drillholes
-----------------------

.. code-block:: python

    >>> dhs = con.find_wells("6728-3555")
    >>> df = con.replacement_drillholes_by_dh_no(dhs)
    >>> print(df)
        dh_no unit_hyphen  new_dh_no new_unit_hyphen replaced_from
    0  203161   6728-3555     362448       6728-4467    2021-07-04

