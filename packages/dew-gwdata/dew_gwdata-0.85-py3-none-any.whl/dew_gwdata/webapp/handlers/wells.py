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


def run_wells_query(conn, query_name, args):
    if len(args):
        return getattr(conn, query_name)(args)
    else:
        cols, _, _ = parse_query_metadata(load_predefined_query(query_name))
        return pd.DataFrame(columns=cols)


@router.get("/wells_summary")
def wells_summary(
    request: Request,
    query: Annotated[queries.Wells, Depends()],
):
    db = connect_to_sageodata(service_name=query.env)
    wells, name, name_safe, query_params = query.find_wells()
    dh_nos = wells.dh_no.unique()
    title = name
    df = run_wells_query(db, "wells_summary", dh_nos)

    df = df.sort_values(
        [query.sort], ascending=True if query.order.startswith("asc") else False
    )
    cols = [
        "dh_no",
        "unit_hyphen",
        "obs_no",
        "dh_name",
        "aquifer",
        "latest_status",
        "latest_swl",
        "latest_tds",
        "purpose",
        "owner",
        "orig_drilled_depth",
        "orig_drilled_date",
        "latest_cased_to",
        "comments",
        # "pwa",
        # "pwra",
    ]

    df_for_table = df[cols]
    title_series = df_for_table.apply(
        lambda well: (
            f'<nobr><a href="/app/well_summary?dh_no={well.dh_no}&env={query.env}">'
            f'{webapp_utils.make_dh_title(well, elements=("unit_no", "obs_no"))}</a></nobr>'
        ),
        axis=1,
    )
    df_for_table.insert(0, "title", title_series)
    df_for_table = df_for_table.drop(["unit_hyphen", "obs_no"], axis=1)
    df_for_table.insert(4, "suburb", gd.locate_wells_in_suburbs(df_for_table))
    table = webapp_utils.frame_to_html(df_for_table)

    egis_layer_definition_query = (
        "DHNO IN (" + ",".join([str(dh_no) for dh_no in df.dh_no]) + ")"
    )

    return templates.TemplateResponse(
        "wells_summary.html",
        {
            "request": request,
            "env": query.env,
            "title": title,
            "query": query,
            "redirect_to": "wells_summary",
            "singular_redirect_to": "well_summary",
            "plural_redirect_to": "wells_summary",
            "wells_title": title,
            "wells_query_params": query_params,
            "wells": df,
            "wells_table": table,
            "egis_layer_definition_query": egis_layer_definition_query,
        },
    )


@router.get("/wells_ownership_status")
def wells_ownership_status(
    request: Request,
    query: Annotated[queries.Wells, Depends()],
):
    db = connect_to_sageodata(service_name=query.env)
    wells, name, name_safe, query_params = query.find_wells()
    dh_nos = wells.dh_no.unique()
    title = name
    df = run_wells_query(db, "wells_summary", dh_nos)

    df = df.sort_values(
        [query.sort], ascending=True if query.order.startswith("asc") else False
    )

    df_for_table = df[
        [
            "dh_no",
            "unit_hyphen",
            "obs_no",
            "dh_name",
            "aquifer",
            "orig_drilled_depth",
            "orig_drilled_date",
            "purpose",
            "latest_status",
            "owner",
            "state_asset",
            "state_asset_status",
            "state_asset_retained",
            "state_asset_comments",
            "comments",
        ]
    ]
    title_series = df_for_table.apply(
        lambda well: (
            f'<nobr><a href="/app/well_summary?dh_no={well.dh_no}&env={query.env}">'
            f'{webapp_utils.make_dh_title(well, elements=("unit_no", "obs_no"))}</a></nobr>'
        ),
        axis=1,
    )
    df_for_table.insert(0, "title", title_series)
    df_for_table = df_for_table.drop(["unit_hyphen", "obs_no"], axis=1)
    df_for_table.insert(4, "suburb", gd.locate_wells_in_suburbs(df_for_table))
    table = webapp_utils.frame_to_html(df_for_table)

    egis_layer_definition_query = (
        "DHNO IN (" + ",".join([str(dh_no) for dh_no in df.dh_no]) + ")"
    )

    return templates.TemplateResponse(
        "wells_ownership_status.html",
        {
            "request": request,
            "env": query.env,
            "title": title,
            "query": query,
            "redirect_to": "wells_ownership_status",
            "singular_redirect_to": "well_summary",
            "plural_redirect_to": "wells_ownership_status",
            "wells_title": title,
            "wells_query_params": query_params,
            "wells": df,
            "wells_table": table,
            "egis_layer_definition_query": egis_layer_definition_query,
        },
    )


@router.get("/wells_data_available")
def wells_data_available(
    request: Request,
    query: Annotated[queries.Wells, Depends()],
):
    db = connect_to_sageodata(service_name=query.env)
    wells, name, name_safe, query_params = query.find_wells()
    dh_nos = wells.dh_no.unique()
    title = name

    summ = run_wells_query(db, "wells_summary", dh_nos)
    data = run_wells_query(db, "data_available", dh_nos)

    summ = summ.sort_values(
        [query.sort], ascending=True if query.order.startswith("asc") else False
    )

    col_to_endpoint_map = {
        "drill_or_lith_logs": "well_drillhole_logs",
        "strat_or_hydro_logs": "well_drillhole_logs",
        "water_levels": "well_manual_water_level",
        "elev_surveys": "well_summary",
        "aquarius_flag": "well_combined_water_level",
        "salinities": "well_salinity",
        "water_cuts": "well_construction",
        "geophys_logs": "well_geophysical_logs",
        "dh_docimg_flag": "well_drillhole_document_images",
        # "photo_flag": "",
    }
    for col, endpoint in col_to_endpoint_map.items():
        data[col] = data.apply(
            lambda row: (
                f'<a href="/app/{endpoint}?dh_no={row.dh_no}&env={query.env}">{row[col]}</a>'
                if row[col] > 0
                else 0
            ),
            axis=1,
        )

    summ_keep = [
        "dh_no",
        "unit_hyphen",
        "obs_no",
        "dh_name",
        "aquifer",
        "orig_drilled_depth",
        "orig_drilled_date",
    ]
    summ["orig_drilled_depth"] = summ.orig_drilled_depth.apply(
        lambda v: f"{v:.02f}" if not pd.isnull(v) else ""
    )
    df_for_table = pd.merge(summ[summ_keep], data, on="dh_no")

    title_series = df_for_table.apply(
        lambda well: (
            f'<nobr><a href="/app/well_summary?dh_no={well.dh_no}&env={query.env}">'
            f'{webapp_utils.make_dh_title(well, elements=("unit_no", "obs_no"))}</a></nobr>'
        ),
        axis=1,
    )
    df_for_table.insert(0, "title", title_series)
    df_for_table = df_for_table.drop(["unit_hyphen", "obs_no"], axis=1)
    df_for_table.insert(4, "suburb", gd.locate_wells_in_suburbs(df_for_table))

    def series_styler(series):
        def value_function(value):
            if value == 0:
                return "border: 1px solid grey;"
            else:
                return "background-color: lightgreen; border: 1px solid grey;"

        return series.apply(value_function)

    apply_colours_to = [
        c
        for c in df_for_table.columns
        if not c in summ.columns and not c in ("title", "suburb")
    ]

    table = webapp_utils.frame_to_html(
        df_for_table,
        apply=series_styler,
        apply_kws=dict(
            axis=1,
            subset=apply_colours_to,
        ),
    )

    egis_layer_definition_query = (
        "DHNO IN (" + ",".join([str(dh_no) for dh_no in summ.dh_no]) + ")"
    )

    return templates.TemplateResponse(
        "wells_data_available.html",
        {
            "request": request,
            "env": query.env,
            "title": title,
            "query": query,
            "redirect_to": "wells_data_available",
            "singular_redirect_to": "well_summary",
            "plural_redirect_to": "wells_data_available",
            "wells_title": title,
            "wells_query_params": query_params,
            "wells": summ,
            "wells_table": table,
            "egis_layer_definition_query": egis_layer_definition_query,
        },
    )


@router.get("/wells_driller_info")
def wells_driller_info(
    request: Request,
    query: Annotated[queries.Wells, Depends()],
):
    db = connect_to_sageodata(service_name=query.env)
    wells, name, name_safe, query_params = query.find_wells()
    dh_nos = wells.dh_no.unique()
    title = name
    summ = run_wells_query(db, "wells_summary", dh_nos)

    summ = summ.sort_values(
        [query.sort], ascending=True if query.order.startswith("asc") else False
    )
    const = db.construction_events(dh_nos)
    const = const[const.event_type == "C"]
    gd.add_construction_activity_column(const)

    summ_cols = [
        "dh_no",
        "unit_hyphen",
        "obs_no",
        "dh_name",
        "aquifer",
        "latest_tds",
        "purpose",
        # "comments",
    ]
    const_cols = [
        "dh_no",
        "completion_date",
        "orig_flag",
        "activity",
        "wcr_id",
        "permit_no",
        "driller_name",
        "total_depth",
        "comments",
    ]

    summ_for_merge = summ[summ_cols].rename(columns={"comments": "dh_comment"})
    const_for_merge = const[const_cols].rename(
        columns={"comments": "construction_comment"}
    )

    df_for_table = pd.merge(summ_for_merge, const_for_merge, on="dh_no")

    title_series = df_for_table.apply(
        lambda well: (
            f'<nobr><a href="/app/well_summary?dh_no={well.dh_no}&env={query.env}">'
            f'{webapp_utils.make_dh_title(well, elements=("unit_no", "obs_no"))}</a></nobr>'
        ),
        axis=1,
    )

    def format_date(x):
        if x is None:
            return "[missing]"
        else:
            return pd.Timestamp(x).strftime("%d/%m/%Y")

    df_for_table.loc[
        df_for_table.completion_date.notnull(), "completion_date"
    ] = df_for_table.loc[df_for_table.completion_date.notnull()].apply(
        lambda row: f'<a href="/app/well_construction?dh_no={row.dh_no}">{format_date(row.completion_date)}</a>',
        axis=1,
    )
    df_for_table.insert(0, "title", title_series)
    df_for_table = df_for_table.fillna("")
    df_for_table = df_for_table.drop(["unit_hyphen", "obs_no"], axis=1)
    df_for_table.insert(4, "suburb", gd.locate_wells_in_suburbs(df_for_table))
    df_for_table = df_for_table.set_index(
        ["title", "dh_no", "dh_name", "aquifer", "suburb", "latest_tds", "purpose"]
    )
    table = webapp_utils.frame_to_html(df_for_table)

    egis_layer_definition_query = (
        "DHNO IN (" + ",".join([str(dh_no) for dh_no in dh_nos]) + ")"
    )

    return templates.TemplateResponse(
        "wells_summary.html",
        {
            "request": request,
            "env": query.env,
            "title": title,
            "query": query,
            "redirect_to": "wells_driller_info",
            "singular_redirect_to": "well_summary",
            "plural_redirect_to": "wells_driller_info",
            "wells_title": title,
            "wells_query_params": query_params,
            "wells": summ,
            "wells_table": table,
            "egis_layer_definition_query": egis_layer_definition_query,
        },
    )


@router.get("/wells_in_group")
def wells_in_group(
    request: Request,
    query: Annotated[queries.Wells, Depends()],
):
    query.group_code = query.group_code.upper()
    db = connect_to_sageodata(service_name=query.env)
    wells, name, name_safe, query_params = query.find_wells()
    dh_nos = wells.dh_no.unique()
    title = name

    groups = db.group_details()
    if not query.group_code in groups.group_code.unique():
        return RedirectResponse(
            f"/app/wells_summary?{query_params}&error_message=Group code must be specified - please search or filter for group in the query form above."
        )
    group = groups[groups.group_code == query.group_code].iloc[0]
    dhs = run_wells_query(db, "wells_in_groups", [query.group_code])
    dhs = dhs[dhs.dh_no.isin(dh_nos)]

    print(dhs)

    dhs["dh_comments"] = dhs.dh_comments.fillna("")

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
            f'<nobr><a href="/app/well_summary?dh_no={well.dh_no}&env={query.env}">'
            f'{webapp_utils.make_dh_title(well, elements=("unit_no", "obs_no"))}</a></nobr>'
        ),
        axis=1,
    )
    dhs.insert(0, "title", title_series)
    dhs = dhs.drop(["well_id", "unit_hyphen", "obs_no"], axis=1)
    dhs.insert(4, "suburb", gd.locate_wells_in_suburbs(dhs))
    dhs_table = webapp_utils.frame_to_html(dhs[cols])

    return templates.TemplateResponse(
        "wells_summary.html",
        {
            "request": request,
            "env": query.env,
            "redirect_to": "wells_in_group",
            "singular_redirect_to": "well_summary",
            "plural_redirect_to": "wells_in_group",
            "query": query,
            "wells": dhs,
            "wells_title": title,
            "wells_query_params": query_params,
            "group": group,
            "dhs": dhs,
            "wells_table": dhs_table,
            "group_code": query.group_code,
            "swl_status": query.swl_status,
            "tds_status": query.tds_status,
            "swl_freq": query.swl_freq,
            "tds_freq": query.tds_freq,
            "filter_group_comment": query.filter_group_comment,
        },
    )


# @router.get("/wells_geojson_summary")
# def wells_map(
#     request: Request,
#     query: Annotated[queries.Wells, Depends()],
# ):
#     db = connect_to_sageodata(service_name=query.env)
#     wells, name, name_safe, query_params = query.find_wells()
#     dh_nos = wells.dh_no.unique()
#     title = name

#     df = run_wells_query(db, "wells_summary", dh_nos)

#     df = df.sort_values([query.sort])

#     features = []
#     for idx, row in df.iterrows():
#         feature = Feature(geometry=Point(()))

#     return templates.TemplateResponse(
#         "wells_map.html",
#         {
#             "request": request,
#             "query": query,
#             "env": query.env,
#             "redirect_to": "wells_map",
#             "singular_redirect_to": "well_summary",
#             "plural_redirect_to": "wells_map",
#             "title": title,
#             "wells_title": title,
#             "wells_query_params": query_params,
#             "wells": df,
#         },
#     )


@router.get("/wells_drillhole_notes")
def wells_drillhole_notes(
    request: Request,
    query: Annotated[queries.Wells, Depends()],
):
    db = connect_to_sageodata(service_name=query.env)
    wells, name, name_safe, query_params = query.find_wells()
    dh_nos = wells.dh_no.unique()
    title = name
    df = run_wells_query(db, "wells_summary", dh_nos)

    df = df.sort_values(
        [query.sort], ascending=True if query.order.startswith("asc") else False
    )

    df2 = db.wells_summary(dh_nos)
    notes = db.drillhole_notes(dh_nos)

    df3 = pd.merge(
        df2,
        notes[
            [
                "dh_no",
                "note_date",
                "note",
                "author",
                "created_by",
                "creation_date",
                "modified_by",
                "modified_date",
            ]
        ],
        on="dh_no",
        how="outer",
    )

    df3 = df3.sort_values(["dh_no", "note_date"], ascending=False)

    def safe_datefmt(v):
        try:
            return v.strftime("%d/%m/%Y")
        except:
            return ""

    df3["note_date"] = df3.note_date.apply(lambda v: f"{safe_datefmt(v)}<wbr>")

    df_for_table = df3[
        [
            "dh_no",
            "unit_hyphen",
            "obs_no",
            "dh_name",
            "aquifer",
            "note_date",
            "note",
            "author",
        ]
    ]
    title_series = df_for_table.apply(
        lambda well: (
            f'<nobr><a href="/app/well_summary?dh_no={well.dh_no}&env={query.env}">'
            f'{webapp_utils.make_dh_title(well, elements=("unit_no", "obs_no"))}</a></nobr>'
        ),
        axis=1,
    )
    df_for_table.insert(0, "title", title_series)
    df_for_table = df_for_table.drop(["unit_hyphen", "obs_no"], axis=1)
    df_for_table.insert(4, "suburb", gd.locate_wells_in_suburbs(df_for_table))
    df_for_table = df_for_table.set_index(["title", "dh_no", "dh_name", "aquifer", "suburb", "note_date"])

    table = webapp_utils.frame_to_html(df_for_table)

    egis_layer_definition_query = (
        "DHNO IN (" + ",".join([str(dh_no) for dh_no in df.dh_no]) + ")"
    )

    return templates.TemplateResponse(
        "wells_drillhole_notes.html",
        {
            "request": request,
            "env": query.env,
            "title": title,
            "query": query,
            "redirect_to": "wells_drillhole_notes",
            "singular_redirect_to": "well_summary",
            "plural_redirect_to": "wells_drillhole_notes",
            "wells_title": title,
            "wells_query_params": query_params,
            "wells": df,
            "wells_table": table,
            "egis_layer_definition_query": egis_layer_definition_query,
        },
    )
