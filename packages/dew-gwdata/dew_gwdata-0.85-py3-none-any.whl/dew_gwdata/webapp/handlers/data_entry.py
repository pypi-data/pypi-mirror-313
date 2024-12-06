import datetime
from pathlib import Path
from typing import Annotated

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


@router.get("/salinity_data_entry_by_day")
def salinity_data_entry_by_day(
    request: Request,
    start_timestamp: str = "2023-01-01",
    end_timestamp: str = "today",
    env: str = "PROD",
):
    if start_timestamp == "":
        start_timestamp = "1997-01-01"
    if end_timestamp == "today" or end_timestamp == "":
        end_timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    db = connect_to_sageodata(service_name=env)
    df = db.salinity_data_entry_from_year(start_timestamp, end_timestamp)
    if len(df):
        df["count_unique_wells"] = df.apply(
            lambda row: f"<a href='/app/wells_summary?salinity_creation_date={row.creation_date.strftime('%Y-%m-%d')}&salinity_created_by={row.created_by}&env={env}'>{row.count_unique_wells}</a>",
            axis=1,
        )

    table = webapp_utils.frame_to_html(df)

    return templates.TemplateResponse(
        "salinity_data_entry_by_day.html",
        {
            "request": request,
            "env": env,
            "redirect_to": "well_summary",
            "singular_redirect_to": "well_summary",
            "plural_redirect_to": "wells_summary",
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "table": table,
        },
    )
