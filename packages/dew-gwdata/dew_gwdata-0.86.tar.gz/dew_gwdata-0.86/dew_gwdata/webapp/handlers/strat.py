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


@router.get("/strat_units")
def strat_units(
    request: Request,
    query: Annotated[queries.StratUnits, Depends()],
):
    strat_unit_nos = query.find_strat_units()
    db = connect_to_sageodata(service_name=query.env)
    details = db.strat_unit_details(strat_unit_nos)
    details["map_symbol"] = details.apply(
        lambda row: f"<a href='/app/strat_unit?strat_unit_no={row.strat_unit_no}&env={query.env}'>{row.map_symbol}</a>",
        axis=1,
    )
    table = webapp_utils.frame_to_html(details)

    return templates.TemplateResponse(
        "strat_units.html",
        {
            "request": request,
            "env": query.env,
            "redirect_to": "strat_units",
            "singular_redirect_to": "well_summary",
            "plural_redirect_to": "wells_summary",
            "details": details,
            "table": table,
            "map_symbol": query.map_symbol,
            "strat_name": query.strat_name,
        },
    )


@router.get("/strat_unit")
def strat_unit(request: Request, strat_unit_no: int, env: str = "PROD"):
    db = connect_to_sageodata(service_name=env)
    details = db.strat_unit_details([strat_unit_no]).iloc[0]
    notes = db.strat_unit_notes([strat_unit_no])
    notes = notes[
        [
            "note_type",
            "desc_type",
            "note",
            "created_by",
            "creation_date",
            "modified_by",
            "modified_date",
        ]
    ]
    aq = db.strat_unit_to_aquifer_unit(strat_unit_no)
    # if len(aq):
    #     aq["aquifer_code"] = aq.apply(lambda row: f"<a href='/app/aquifer_unit?strat_unit_no={row.aquifer_strat_unit_no}&hydro_subunit_code={row.aquifer_hydro_subunit_code}&env={env}'>{row.aquifer_code}</a>", axis=1)
    aq = aq[["aquifer_code", "hydro_subunit_desc"]]

    details[
        "agso_number"
    ] = f"<a href='https://asud.ga.gov.au/search-stratigraphic-units/results/{details.agso_number}'>{details.agso_number}</a>"

    details_table = webapp_utils.series_to_html(details)
    notes_table = webapp_utils.frame_to_html(notes)
    aq_table = webapp_utils.frame_to_html(aq)

    return templates.TemplateResponse(
        "strat_unit.html",
        {
            "request": request,
            "env": env,
            "redirect_to": "strat_unit",
            "singular_redirect_to": "well_summary",
            "plural_redirect_to": "wells_summary",
            "details": details,
            "details_table": details_table,
            "notes_table": notes_table,
            "aq": aq,
            "aq_table": aq_table,
            "map_symbol": details.map_symbol,
            "strat_name": "%",
        },
    )
