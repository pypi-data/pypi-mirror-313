Accessing groundwater data
==========================

dew_gwdata provides access to both SA Geodata and Aquarius. The former contains
most relevant groundwater data, and Aquarius is currently the location
of most continuous logger data.

SA Geodata is an enterprise Oracle database. You need to be on the SA Government
intranet to access it. All of the functions that access it require a connection,
which you create quite easily:

.. code-block:: python

    >>> import dew_gwdata as gd
    >>> db = gd.sageodata()
    >>> db
    <sageodata_db.SAGeodataConnection at 0x0014456>

This connection will expire after 6+ hours, so if you leave your Python
session running overnight, you may need to recreate the ``db`` object.

Identifying wells
--------------------

Generally we are looking for data at the level of one or more groundwater
wells. These can be identified in a variety of ways, and there is one function
that is useful for this.

Let's start with a list of wells: G662801265, 6628-14328, YAT30, and ULE 205.

.. code-block:: python

    >>> wells = db.find_wells(": G662801265, 6628-14328, YAT30, and ULE 205.")
    >>> wells
    ["6628-1265",
     "YAT030",
     "MOR201",
     "ULE205"]

Each well in this list has the columns of ``dhdb.dd_drillhole_vw`` and
``dhdb.dd_drillhole_summary_vw`` as attributes:

.. code-block:: python

    >>> well = wells[2]
    >>> well.title
    "6628-14328 / MOR201"
    >>> well.presc_water_res_area_code
    'Barossa Valley'

The predefined queries which are running behind the scenes have some helpful
additional attributes which you may find useful:

.. code-block:: python

    >>> well.aquifer
    'Tomr(Lower)'

Every attribute on an individual well here can be accessed on the list of
all the wells:

.. code-block:: python

    >>> wells.aquifer
    ['Tomw(T2)', 'Tomw(T1)', 'Tomr(Lower)', 'Qpcb+Tbw']

Fetching water level data
---------------------------

Water level data from both SA Geodata and Aquarius can be obtained
for one or more wells as a :class:`pandas.DataFrame` by using a the simple
function :func:`dew_gwdata.fetch_wl_data`.

.. code-block:: python

    >>> df = gd.fetch_wl_data(wells)

Amongst other things, this function will convert Aquarius DTW data to RSWL for
you based on the elevation records in SA Geodata. 
.. By default it will only ask
.. Hydstra for the average DTW once every 5 days. You can obtain more frequent
.. readings (at the expense of up to a few minutes delay, depending on how many
.. years of data there is) using keyword arguments:

.. .. code-block:: python

..     >>> df = gd.fetch_wl_data(wells, interval="hour", multiplier=12)

.. See :func:`dew_gwdata.fetch_hydstra_dtw_data` for more information.

Downloading other data from SA Geodata
----------------------------------------

There are a range of predefined queries to which you can pass list of wells,
and receive data back:

.. code-block:: python

    >>> df = db.water_levels(wells)
    >>> df.info()
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 685 entries, 0 to 684
    Data columns (total 24 columns):
    dh_no               685 non-null int64
    aquifer             685 non-null object
    unit_long           685 non-null int64
    amg_easting         685 non-null float64
    amg_northing        685 non-null float64
    amg_zone            685 non-null int64
    unit_hyphen         685 non-null object
    obs_no              684 non-null object
    obs_date            685 non-null datetime64[ns]
    swl                 682 non-null float64
    dtw                 683 non-null float64
    rswl                682 non-null float64
    pressure            0 non-null object
    temperature         0 non-null object
    dry_ind             0 non-null object
    anomalous_ind       685 non-null object
    pumping_ind         685 non-null object
    measured_during     685 non-null object
    data_source_code    685 non-null object
    comments            9 non-null object
    created_by          685 non-null object
    creation_date       685 non-null datetime64[ns]
    modified_by         505 non-null object
    modified_date       505 non-null datetime64[ns]
    dtypes: datetime64[ns](3), float64(5), int64(3), object(13)
    memory usage: 93.7+ KB

The full list of predefined query methods, the arguments that they take,
and the data fields that they return, are documented at :ref:`predefined-queries-label`.

You can also run any SQL query through
:meth:`dew_gwdata.SAGeodataConnection.query`:

.. code-block:: python

    >>> db.query(db.SQL("select * from dhdb.dd_dh_group_vw where drillhole_no = 61297"))
    drillhole_no group_code stand_water_level_status salinity_status swl_freq  \
    0         61297    BAROSSA                        C               H        6
    1         61297    BRS_CUR                        N               N     None
    2         61297    BVHYDAT                        N               N     None
    3         61297        EPA                        N               C     None
    4         61297   GW_ASSET                        C               C     None
    5         61297       SPBV                        N               N     None

    salinity_freq comments confidential_flag created_by       creation_date  \
    0          None     None                 N       DHDB 1997-07-26 12:48:14
    1          None     None                 N      GADZU 2003-02-10 09:22:28
    2          None     None                 N       DHDB 1995-05-16 15:43:54
    3             R  Barossa                 N      GASLE 2005-11-17 08:17:21
    4          None     None                 N      GAHZU 2003-11-21 15:23:55
    5          None     None                 N       DHDB 1997-07-26 12:54:01

    modified_by       modified_date min_upload_no route_order
    0  MHUTCHESSON 2018-08-03 13:36:09          None        None
    1         None                 NaT          None        None
    2         None                 NaT          None        None
    3        GASLE 2005-11-21 08:14:27          None        None
    4        GAHZU 2005-06-14 13:07:01          None        None
    5         None                 NaT          None        None


