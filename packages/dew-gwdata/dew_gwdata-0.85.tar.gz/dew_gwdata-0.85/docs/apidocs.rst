dew_gwdata developer API
========================

Also see :mod:`sageodata_db`.

Groundwater data access and processing
----------------------------------------------------------

.. autofunction:: dew_gwdata.fetch_wl_data
.. autofunction:: dew_gwdata.transform_dtw_to_rswl

Aquarius data access
----------------------------------------------------------
.. .. autofunction:: dew_gwdata.
.. .. autoclass:: dew_gwdata.
..     :members:

.. autofunction:: dew_gwdata.register_aq_password
.. autofunction:: dew_gwdata.get_password
.. autofunction:: dew_gwdata.convert_aq_timestamp
.. autofunction:: dew_gwdata.convert_timestamps
.. autofunction:: dew_gwdata.convert_GetLocationData_to_series
.. autofunction:: dew_gwdata.convert_GetTimeseriesMetadata_to_series
.. autofunction:: dew_gwdata.identify_aq_locations
.. autofunction:: dew_gwdata.apply_time_periods
.. autofunction:: dew_gwdata.convert_timeseries_relationships_to_graphs
.. autofunction:: dew_gwdata.draw_timeseries_relationship_graph
.. autofunction:: dew_gwdata.unstack_aq_tags
.. autofunction:: dew_gwdata.get_swims_metadata_connection

.. autoclass:: dew_gwdata.Endpoint
    :members:
.. autoclass:: dew_gwdata.DEWAquariusServer
    :members:
.. autoclass:: dew_gwdata.DEWAquarius
    :members:

.. Hydstra access
.. --------------

.. .. autofunction:: dew_gwdata.fetch_hydstra_dtw_data
.. .. autofunction:: dew_gwdata.hydstra_quality
.. .. autofunction:: dew_gwdata.resample_logger_wls

Geophysical logging data archive ("gtslogs")
----------------------------------------------------------

.. autofunction:: dew_gwdata.las_to_log_type
.. autofunction:: dew_gwdata.get_las_metadata

.. autoclass:: dew_gwdata.GtslogsArchiveFolder
    :members:
.. autoclass:: dew_gwdata.GLJobs
    :members:
.. autoclass:: dew_gwdata.GLJob
    :members:
.. autoclass:: dew_gwdata.LogDataFile
    :members:
.. autoclass:: dew_gwdata.CSVLogDataFile
    :members:
.. autoclass:: dew_gwdata.LASLogDataFile
    :members:

WILMA reporting
-----------------

.. autofunction:: dew_gwdata.parse_wilma_csv_export
.. autofunction:: dew_gwdata.read_allocation_csv
.. autofunction:: dew_gwdata.read_usage_csv
.. autofunction:: dew_gwdata.sourcedesc_to_unit_hyphen
.. autofunction:: dew_gwdata.read_timestamped_allocation_csv
.. autofunction:: dew_gwdata.read_timestamped_usage_csv
.. autofunction:: dew_gwdata.read_wilma_licence_parcel_shapefile
.. autofunction:: dew_gwdata.read_timestamped_wilma_licence_parcel_shapefile
.. autofunction:: dew_gwdata.iter_wilma_downloads
.. autofunction:: dew_gwdata.read_all_wilma_data
.. autofunction:: dew_gwdata.read_all_wilma_data_to_flat
.. autofunction:: dew_gwdata.filter_to_keep_latest_download
.. autofunction:: dew_gwdata.identify_dtypes
.. autofunction:: dew_gwdata.update_db
.. autofunction:: dew_gwdata.connect_to_wilma_sqlite_db
.. autofunction:: dew_gwdata.read_from_wilma_sqlite_db
.. autofunction:: dew_gwdata.query_alloc_for_licence_no
.. autofunction:: dew_gwdata.query_usage_for_unit_hyphen
.. autofunction:: dew_gwdata.query_usage_for_licence_no
.. autofunction:: dew_gwdata.total_taking
.. autofunction:: dew_gwdata.summarise_usage_table
.. autofunction:: dew_gwdata.summarise_taking_alloc_history
.. autofunction:: dew_gwdata.plot_alloc_usage_for_licenced_well
.. autofunction:: dew_gwdata.plot_alloc_usage_for_licence
.. autofunction:: dew_gwdata.plot_usage_for_licenced_well

Stratigraphy and hydrostratigraphy
---------------------------------------------------

.. autoclass:: dew_gwdata.StratigraphyHierarchy
    :members:
.. autoclass:: dew_gwdata.Hydrostratigraphy
    :members:

Well construction - production zone
--------------------------------------

.. autoclass:: dew_gwdata.ProductionZoneData
    :members:

