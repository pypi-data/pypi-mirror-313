from typing import Annotated
import logging
import fnmatch

import pandas as pd
from fastapi import Query

from pydantic import BaseModel

from dew_gwdata import sageodata as connect_to_sageodata
from dew_gwdata.webapp import utils as webapp_utils


logger = logging.getLogger(__name__)

FIND_WELLS_COLUMN_MAPPER = {
    "unit_no.hyphen": "unit_hyphen",
    "unit_no.long": "unit_long",
    "obs_no.id": "obs_no",
}


class Wells(BaseModel):
    env: str = "PROD"

    # SEARCH FOR WELLS - GROUPED EXCLUSIVELY
    # --------------------------------------

    # Group 1 - search by ID
    idq: str = ""
    idq_unit_no: bool = True
    idq_dh_no: bool = False
    idq_obs_no: bool = True
    idq_dh_no_as_req: bool = True
    # Additionally, optionally, find wells within X of the first match
    idq_distance: float = 0

    # Group 2 - search by direct reference to drillhole numbers
    url_str: str = ""

    # Group 3 - search by fragment of drillhole name
    name_fragment: str = ""

    # Group 4 - search wells by date of salinity sample creation
    salinity_creation_date: str = ""
    salinity_created_by: str = ""

    # Group 5 - search by strat unit (in logs)
    strat_map_symbol: str = ""
    strat_unit_no: int = 0

    # Group 6 - search by hydrostrat log unit
    hydrostrat_aquifer_code: str = ""
    hydro_strat_unit_no: int = 0
    hydro_subunit_code: str = ""

    # Group 7 - search by current aquifer monitored code
    aq_mon: str = ""

    # Group 8 - Find wells by aquifer code part (current or historical)
    aquifer_code: str = ""
    include_historical_aquifers: bool = False

    # Group 9 - find wells by group code
    group_code: str = ""
    swl_status: str = "C,H,N"
    tds_status: str = "C,H,N"
    swl_freq: str = "1,2,3,4,6,12,24,R,S,blank"
    tds_freq: str = "1,2,3,4,6,12,24,R,S,blank"
    filter_group_comment: str = "*"

    # Group 10 - arbitrary SQL
    sql: str = ""

    status_code: str = ""

    # FILTER OPTIONS - reduce list of wells through filter options
    # ------------------------------------------------------------

    # None currently

    # SORT OPTIONS
    # ------------

    # To be implemented

    sort: str = "unit_hyphen"
    order: str = "ascending"

    # OTHER OPTIONS
    # -------------
    error_message: str = ""

    def find_wells(self):
        db = connect_to_sageodata(service_name=self.env)

        # PRE-PROCESS SEARCH OPTIONS
        # --------------------------

        if self.strat_map_symbol and not self.strat_unit_no:
            df = db.strat_unit_by_map_symbol(self.strat_map_symbol)
            if len(df):
                self.strat_unit_no = df.map_symbol.iloc[0]
        if self.hydrostrat_aquifer_code and not (
            self.hydro_strat_unit_no and self.hydro_subunit_code
        ):
            df = db.strat_unit_by_map_symbol(self.strat_map_symbol)
            if len(df):
                self.strat_unit_no = df.map_symbol.iloc[0]

        # SEARCH FOR WELLS
        # ----------------
        wells = None

        if self.idq.strip():
            logger.debug(f"Running Wells query for idq={self.idq}")
            id_types = []
            if self.idq_unit_no:
                id_types.append("unit_no")
            if self.idq_obs_no:
                id_types.append("obs_no")
            if self.idq_dh_no:
                id_types.append("dh_no")

            logger.debug(f"id_types requested: {id_types}")

            if self.idq_dh_no_as_req:
                # Try and search dh_no only if there is no result
                wells = db.find_wells(
                    self.idq, types=[t for t in id_types if not t == "dh_no"]
                ).df()
                if len(wells) == 0:
                    wells = db.find_wells(self.idq, types=id_types).df()
            else:
                wells = db.find_wells(self.idq, types=id_types).df()

            if self.idq_distance > 0:
                wells = db.drillhole_within_distance(wells.dh_no[0], self.idq_distance)
            else:
                wells = db.drillhole_details(wells.dh_no)

            x = str(self.idq)
            if len(x) > 12:
                x = x[:9] + "..."

            query_params = [
                f"idq={self.idq}",
                f"idq_unit_no={int(self.idq_unit_no)}",
                f"idq_obs_no={int(self.idq_obs_no)}",
                f"idq_dh_no={int(self.idq_dh_no)}",
                f"idq_dh_no_as_req={int(self.idq_dh_no_as_req)}",
            ]

            if self.idq_distance:
                name = f"Wells within {self.idq_distance} km of '{x}'"
                name_safe = f"{self.idq_distance}km_from_" + x.replace(" ", "_")
            else:
                name = f"Search '{x}'"
                name_safe = "search_" + x.replace(" ", "_")

        elif self.url_str:
            logger.debug(f"Running Wells query for url_str={self.url_str}")
            dh_nos = webapp_utils.urlstr_to_dhnos(self.url_str)
            wells = db.drillhole_details(dh_nos)
            name = f"Direct selection"
            name_safe = self.url_str
            query_params = [f"url_str={self.url_str}"]

        elif self.name_fragment:
            logger.debug(f"Running Wells query for name_fragment={self.name_fragment}")
            wells = db.drillhole_details_by_name_search(self.name_fragment)
            name = f"Search for '{self.name_fragment}'"
            name_safe = f"search_{self.name_fragment}"
            query_params = [f"name_fragment={self.name_fragment}"]

        elif self.salinity_creation_date and self.salinity_created_by:
            logger.debug(
                f"Running Wells query for salinity_creation_date={self.salinity_creation_date} and salinity_created_by={self.salinity_created_by}"
            )
            tstamp = pd.Timestamp(self.salinity_creation_date)
            tstamp_ymd = tstamp.strftime("%Y-%m-%d")
            wells = db.query(
                "select s.drillhole_no as dh_no from sm_sample s "
                "join dd_drillhole d on s.drillhole_no = d.drillhole_no "
                f"where s.creation_date >= to_date('{tstamp_ymd} 00:00', 'YYYY-MM-DD HH24:MI') "
                f"and s.creation_date <= to_date('{tstamp_ymd} 23:59', 'YYYY-MM-DD HH24:MI') "
                f"and s.created_by like '{self.salinity_created_by}' "
                "and d.deletion_ind = 'N' and s.sample_type = 'S' "
            )
            wells = db.drillhole_details(wells)
            name = f"Search for wells with salinity data created on {tstamp.strftime('%d/%m/%y')} by {self.salinity_created_by}"
            name_safe = f"search_tds_{self.salinity_created_by}_{tstamp_ymd}"
            query_params = [
                f"salinity_creation_date={self.salinity_creation_date}",
                f"salinity_created_by={self.salinity_created_by}",
            ]

        elif self.strat_unit_no:
            logger.debug(f"Running Wells query for strat_unit_no={self.strat_unit_no}")
            wells = db.strat_logs_by_strat_unit([self.strat_unit_no])
            st = db.strat_unit_details([self.strat_unit_no])
            if len(st) > 0:
                st = st.iloc[0]
            name = f"Search for '{st.map_symbol}' in a strat log"
            name_safe = f"search_strat_unit_{st.map_symbol}"
            query_params = [f"strat_unit_no={self.strat_unit_no}"]

        elif self.hydro_strat_unit_no:
            logger.debug(
                f"Running Wells query for hydro_strat_unit_no={self.hydro_strat_unit_no}"
            )
            wells = db.hydrostrat_logs_by_strat_unit([self.hydro_strat_unit_no])
            st = db.strat_unit_details([self.hydro_strat_unit_no])
            if len(st) > 0:
                st = st.iloc[0]
            name = f"Search for '{st.map_symbol}' in a hydrostrat log"
            name_safe = f"search_hydro_strat_unit_{st.map_symbol}"
            query_params = [f"hydro_strat_unit_no={self.hydro_strat_unit_no}"]

        elif self.group_code:
            logger.debug(f"Running Wells query for group_code={self.group_code}")
            wells = db.wells_in_groups([self.group_code])

            wells["dh_comments"] = wells.dh_comments.fillna("")

            swl_freqs = [f.strip() for f in self.swl_freq.split(",")]
            tds_freqs = [f.strip() for f in self.tds_freq.split(",")]
            swl_statuses = [s.strip() for s in self.swl_status.split(",")]
            tds_statuses = [s.strip() for s in self.tds_status.split(",")]
            if "blank" in swl_freqs:
                swl_freqs.append(None)
            if "blank" in tds_freqs:
                tds_freqs.append(None)

            wells = wells[wells.swl_freq.isin(swl_freqs)]
            wells = wells[wells.tds_freq.isin(tds_freqs)]
            wells = wells[wells.swl_status.isin(swl_statuses)]
            wells = wells[wells.tds_status.isin(tds_statuses)]
            wells = wells[
                wells.apply(
                    lambda row: fnmatch.fnmatch(
                        row.dh_comments, self.filter_group_comment
                    ),
                    axis=1,
                )
            ]
            name = f"Search group '{self.group_code}'"
            name_safe = f"search_group_{self.group_code}"
            query_params = [
                f"group_code={self.group_code}",
                f"filter_group_comment={self.filter_group_comment}",
                f"swl_status={self.swl_status}",
                f"tds_status={self.tds_status}",
                f"swl_freq={self.swl_freq}",
                f"tds_freq={self.tds_freq}",
            ]

        elif self.aq_mon:
            wells = db.drillholes_by_full_current_aquifer([self.aq_mon])
            name = f"Search for exact aquifer '{self.aq_mon}'"
            name_safe = f"search_exact_aquifer_{self.aq_mon}"
            query_params = [f"aq_mon={self.aq_mon}"]

        elif self.aquifer_code:
            wells = db.drillholes_by_aquifer_all([self.aquifer_code])
            if not self.include_historical_aquifers:
                wells = wells[
                    wells.current_aquifer.str.contains(f"{self.aquifer_code}")
                ]
            name = f"Search for aquifer '{self.aquifer_code}'"
            name_safe = f"search_aquifer_{self.aquifer_code}"
            query_params = [
                f"aq_mon={self.aquifer_code}",
                f"include_historical_aquifers={int(self.include_historical_aquifers)}",
            ]

        elif self.status_code:
            status_codes = [s.strip().upper() for s in self.status_code.split(",")]
            wells = db.drillholes_by_status(status_codes)
            name = f"Search for wells with historical status"
            name_safe = f"search_status_hist_{self.status_code}"
            query_params = [f"status_code={self.status_code}"]

        elif self.sql:
            wells = db.query(self.sql)
            name = f"Search by arbitrary SQL"
            name_safe = f"search_arbitrary_sql"
            query_params = [f"sql={self.sql}"]

        else:
            wells = db.drillhole_details([0])
            name = f"Empty search"
            name_safe = f"empty"
            query_params = [
                f"idq=",
                f"idq_unit_no=1",
                f"idq_obs_no=1",
                f"idq_dh_no=0",
                f"idq_dh_no_as_req=0",
            ]
            self.error_message = "Please enter a search query in one of the boxes under the 'Query form' above."

        # FILTER
        # ------

        # SORT
        # ----

        if self.sort == "dh_no":
            query_params.append("sort=dh_no")
        elif self.sort == "unit_hyphen":
            query_params.append("sort=unit_hyphen")

        name += f" ({len(wells)} wells)" if len(wells) != 1 else " (1 well)"
        if len(wells) == 1 and self.url_str:
            name_safe = f"dh_{wells.dh_no[0]}"
        name_safe = name_safe[:30]
        query_params.append(f"env={self.env}")

        logger.debug(f"query found {len(wells)} drillholes: {wells.dh_no.values}")

        return wells, name, name_safe, "&".join(query_params)


class StratUnits(BaseModel):
    env: str = "PROD"

    map_symbol: str = ""
    strat_name: str = "%"

    def find_strat_units(self):
        db = connect_to_sageodata(service_name=self.env)
        df = db.query(
            f"select strat_unit_no from st_strat_unit "
            f"where map_symbol like '{self.map_symbol}' "
            f"and upper(strat_name) like upper('{self.strat_name}')"
        )
        return list(df.strat_unit_no.values)


class GeophysLogJobs(BaseModel):
    env: str = "PROD"

    # SEARCH FOR WELLS - GROUPED EXCLUSIVELY
    # --------------------------------------

    # Group 1 - search by job number range
    job_no_from: int = None
    job_no_to: int = None

    # Group 2 - search by job number
    job_no: int = None

    # Group 3 - search by discrete job numbers
    jobstr: str = ""

    # Group 4 - search by logged date range
    logged_date_from: str = ""
    logged_date_to: str = ""

    # Group 5 - location search
    location: str = ""

    # FILTER OPTIONS - reduce list of wells through filter options
    # ------------------------------------------------------------

    location_contains: str = ""
    purpose_contains: str = ""
    operator_contains: str = ""
    vehicle_contains: str = ""
    log_depth_min: float = None

    # SORT OPTIONS
    # ------------

    sort: str = "logged_date"
    order: str = "ascending"

    def find_jobs(self):
        db = connect_to_sageodata(service_name=self.env)

        # SEARCH FOR JOBS
        # ----------------
        wells = None

        # Group 1 - search by job number range
        if self.job_no_from or self.job_no_to:
            if not self.job_no_from:
                self.job_no_from = 0
            if not self.job_no_to:
                self.job_no_to = 100000
            df = db.geophys_log_metadata_by_job_no_range(
                self.job_no_from, self.job_no_to
            )
            title = f"Jobs between {self.job_no_from} and {self.job_no_to}"
            query_params = [
                f"job_no_from={self.job_no_from}",
                f"job_no_to={self.job_no_to}",
            ]

        # Group 2 - search by job number
        elif self.job_no:
            df = db.geophys_log_metadata_by_job_no([self.job_no])
            title = f"Job number {self.job_no}"
            query_params = [f"job_no={self.job_no}"]

        elif self.jobstr:
            job_nos = webapp_utils.urlstr_to_dhnos(self.jobstr)
            df = db.geophys_log_metadata_by_job_no(job_nos)
            title = f"Job number selection"
            query_params = [f"jobstr={self.jobstr}"]

        # Group 4 - search by logged date range
        elif self.logged_date_from or self.logged_date_to:
            if not self.logged_date_from:
                self.logged_date_from = "1950-01-01"
            if not self.logged_date_to:
                self.logged_date_to = "2100-01-01"
            logged_date_from = pd.Timestamp(self.logged_date_from)
            logged_date_to = pd.Timestamp(self.logged_date_to)
            df = db.geophys_log_metadata_by_logged_date_range(
                logged_date_from, logged_date_to
            )
            title = f"Jobs logged between {logged_date_from.strftime('%d/%m/%Y')} and {logged_date_to.strftime('%d/%m/%Y')}"
            query_params = [
                f"logged_date_from={self.logged_date_from}",
                f"logged_date_to={self.logged_date_to}",
            ]

        # Group 5 - location search
        elif self.location:
            df = db.geophys_log_metadata_by_location(self.location)
            title = f"Jobs logged at location '{self.location}'"
            query_params = [f"location={self.location}"]

        # FILTER
        # ------

        if self.location_contains:
            df = df[df.location.str.contains(self.location_contains, regex=False)]
            query_params.append(f"location_contains={self.location_contains}")

        if self.purpose_contains:
            df = df[df.purpose.str.contains(self.purpose_contains, regex=False)]
            query_params.append(f"purpose_contains={self.purpose_contains}")

        if self.operator_contains:
            df = df[df.operators.str.contains(self.operator_contains, regex=False)]
            query_params.append(f"operator_contains={self.operator_contains}")

        if self.vehicle_contains:
            df = df[df.vehicle.str.contains(self.vehicle_contains, regex=False)]
            query_params.append(f"vehicle_contains={self.vehicle_contains}")

        if self.log_depth_min:
            df = df[(df.max_log_depth >= self.log_depth_min)]
            query_params.append(f"log_depth_min={self.log_depth_min}")

        # SORT
        # ----

        if self.sort == "dh_no":
            query_params.append("sort=dh_no")
        elif self.sort == "unit_hyphen":
            query_params.append("sort=unit_hyphen")
        elif self.sort == "obs_no":
            query_params.append("sort=obs_no")
        elif self.sort == "logged_date":
            query_params.append("sort=logged_date")

        query_params.append(f"order={self.order}")

        return df, title, "&".join(query_params)
