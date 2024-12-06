from pathlib import Path
from typing import Annotated
import fnmatch

import pandas as pd
from geojson import Feature, Point
from fastapi import APIRouter, Request, Query, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.datastructures import URL

from sageodata_db import connect as connect_to_sageodata
from sageodata_db import load_predefined_query
from sageodata_db.utils import parse_query_metadata

import dew_gwdata as gd
from dew_gwdata.sageodata_datamart import get_sageodata_datamart_connection

from dew_gwdata.webapp import utils as webapp_utils
from dew_gwdata.webapp.models import queries


router = APIRouter(prefix="/app", include_in_schema=False)

templates_path = Path(__file__).parent.parent / "templates"

templates = Jinja2Templates(directory=templates_path)


@router.get("/geophys_logs_summary")
def geophys_logs_summary(
    request: Request,
    query: Annotated[queries.GeophysLogJobs, Depends()],
):
    db = connect_to_sageodata(service_name=query.env)
    df, title, query_params = query.find_jobs()

    df = df.sort_values(query.sort, ascending=query.order == "ascending")

    title_series = df.apply(
        lambda well: (
            f'<nobr><a href="/app/well_summary?dh_no={well.dh_no}&env={query.env}">'
            f'{webapp_utils.make_dh_title(well, elements=("unit_no", "obs_no"))}</a></nobr>'
        ),
        axis=1,
    )
    df.insert(0, "title", title_series)
    df = df.drop(["well_id", "unit_hyphen", "obs_no"], axis=1)
    df.insert(4, "suburb", gd.locate_wells_in_suburbs(df))

    df = df.drop(
        [
            "log_hdr_no",
            "log_easting",
            "log_northing",
            "log_zone",
            "log_latitude",
            "log_longitude",
            "unit_long",
            "easting",
            "northing",
            "zone",
            "latitude",
            "longitude",
        ],
        axis=1,
    )

    table = webapp_utils.frame_to_html(df)

    return templates.TemplateResponse(
        "geophys_logs_summary.html",
        {
            "request": request,
            "env": query.env,
            "redirect_to": "group_summary",
            "singular_redirect_to": "well_summary",
            "plural_redirect_to": "wells_summary",
            "query": query,
            "df": df,
            "table": table,
        },
    )


@router.get("/group_summary")
def group_summary(
    request: Request,
    group_code: str,
    swl_status: str = "C,H,N",
    tds_status: str = "C,H,N",
    swl_freq: str = "1,2,3,4,6,12,24,R,S,blank",
    tds_freq: str = "1,2,3,4,6,12,24,R,S,blank",
    filter_comment: str = "*",
    env: str = "PROD",
):
    group_code = group_code.upper()
    db = connect_to_sageodata(service_name=env)
    groups = db.group_details()
    group = groups[groups.group_code == group_code].iloc[0]
    dhs = db.wells_in_groups([group_code])

    dhs["dh_comments"] = dhs.dh_comments.fillna("")

    swl_freqs = [f.strip() for f in swl_freq.split(",")]
    tds_freqs = [f.strip() for f in tds_freq.split(",")]
    swl_statuses = [s.strip() for s in swl_status.split(",")]
    tds_statuses = [s.strip() for s in tds_status.split(",")]
    if "blank" in swl_freqs:
        swl_freqs.append(None)
    if "blank" in tds_freqs:
        tds_freqs.append(None)

    dhs = dhs[dhs.swl_freq.isin(swl_freqs)]
    dhs = dhs[dhs.tds_freq.isin(tds_freqs)]
    dhs = dhs[dhs.swl_status.isin(swl_statuses)]
    dhs = dhs[dhs.tds_status.isin(tds_statuses)]
    dhs = dhs[
        dhs.apply(lambda row: fnmatch.fnmatch(row.dh_comments, filter_comment), axis=1)
    ]

    cols = [
        "title",
        "dh_no",
        "dh_name",
        "aquifer",
        "suburb",
        "swl_status",
        "swl_freq",
        "tds_status",
        "tds_freq",
        "dh_comments",
        "dh_created_by",
        "dh_creation_date",
        "dh_modified_by",
        "dh_modified_date",
    ]

    title_series = dhs.apply(
        lambda well: (
            f'<nobr><a href="/app/well_summary?dh_no={well.dh_no}&env={env}">'
            f'{webapp_utils.make_dh_title(well, elements=("unit_no", "obs_no"))}</a></nobr>'
        ),
        axis=1,
    )
    dhs.insert(0, "title", title_series)
    dhs = dhs.drop(["well_id", "unit_hyphen", "obs_no"], axis=1)
    dhs.insert(4, "suburb", gd.locate_wells_in_suburbs(dhs))
    dhs_table = webapp_utils.frame_to_html(dhs[cols])

    return templates.TemplateResponse(
        "group_summary.html",
        {
            "request": request,
            "env": env,
            "redirect_to": "group_summary",
            "singular_redirect_to": "well_summary",
            "plural_redirect_to": "wells_summary",
            "group": group,
            "dhs": dhs,
            "dhs_table": dhs_table,
            "group_code": group_code,
            "swl_status": swl_status,
            "tds_status": tds_status,
            "swl_freq": swl_freq,
            "tds_freq": tds_freq,
            "filter_comment": filter_comment,
        },
    )
