from pathlib import Path
from typing import Annotated

import pandas as pd
from geojson import Feature, Point
from fastapi import APIRouter, Request, Query, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.datastructures import URL
import lasio

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


def get_well_metadata(df, dh_no, env="prod"):
    cols = ["dh_no", "unit_hyphen", "obs_no", "dh_name", "aquifer"]

    def check_columns():
        for col in cols:
            if not col in df.columns:
                return False
        return True

    if len(df) and check_columns():
        result = df[cols].iloc[0]
    else:
        db = connect_to_sageodata(service_name=env)
        result = db.wells_summary([dh_no])[cols].iloc[0]
    result["title"] = webapp_utils.make_dh_title(result)
    return result


@router.get("/well_summary")
def well_summary(request: Request, dh_no: int, env: str = "prod") -> str:
    db = connect_to_sageodata(service_name=env)
    well = db.wells_summary([dh_no]).iloc[0]
    groups = db.drillhole_groups([dh_no]).pipe(gd.cleanup_columns)
    notes = db.drillhole_notes([dh_no]).sort_values(["note_date"], ascending=True)
    status = db.drillhole_status([dh_no]).sort_values(["status_date"], ascending=False)
    geophyslogs = db.geophys_log_metadata([dh_no]).sort_values(
        "logged_date", ascending=True
    )
    aqmon = db.aquifers_monitored([dh_no]).sort_values(
        ["aquifer_mon_from"], ascending=False
    )
    files = db.drillhole_file_list([dh_no])
    refs = db.drillhole_document_references([dh_no])
    const = db.construction_events([dh_no]).sort_values(
        "completion_date", ascending=True
    )
    const = gd.add_construction_activity_column(const)
    elev = db.elevation_surveys([dh_no]).assign(**{"ref_height [calculated]": pd.NA})
    elev.loc[
        (~pd.isnull(elev.ground_elev)) & (~pd.isnull(elev.ref_elev)),
        "ref_height [calculated]",
    ] = (
        elev.ref_elev - elev.ground_elev
    )
    groups["group_code"] = groups.group_code.apply(
        lambda grp: f"<a href='/app/group_summary?group_code={grp}&env={env}'>{grp}</a>"
    )
    groups["sort_key"] = groups.group_type.map(
        {"OMN": 0, "PR": 1, "OMH": 2, "GDU": 3, "MDU": 4}
    )
    groups = groups.sort_values(["sort_key", "group_modified_date"])
    groups = groups.drop(
        [
            "well_id",
            "sort_key",
            "dh_created_by",
            "dh_creation_date",
            "dh_modified_by",
            "dh_modified_date",
            "group_created_by",
            "group_creation_date",
            "group_modified_by",
            "group_modified_date",
        ],
        axis=1,
    )

    files["file_name"] = files.apply(
        lambda row: f"<a href='/api/db_file?file_no={row.file_no}'>{row.file_name}</a>",
        axis=1,
    )
    geophyslogs["job_no"] = geophyslogs.job_no.apply(
        lambda job_no: f"<a href='/app/well_geophysical_logs?dh_no={dh_no}&env={env}#{job_no}'>{job_no}</a>"
    )
    const["completion_date_str"] = const.completion_date.apply(
        lambda d: d.strftime("%d/%m/%Y") if not pd.isnull(d) else ""
    )
    const["completion_date"] = const.apply(
        lambda row: f"<a href='/app/well_construction?dh_no={dh_no}&env={env}#{row.completion_no}'>{row.completion_date_str}</a>",
        axis=1,
    )

    def make_envelope_link(ref_id):
        try:
            int_ref_id = int(ref_id)
        except:
            return ref_id
        else:
            url = "https://sarigbasis.pir.sa.gov.au/WebtopEw/ws/samref/sarig1/cat2/ResultSet"
            tag = f"<a href='{url}?w=NATIVE%28%27allfields%2Ctext+ph+is+%27%27Env+{int_ref_id:05.0f}%27%27%27%29'>"
            return f"{tag}{ref_id}</a>"

    refs.loc[refs.ref_type == "ENV", "ref_id"] = refs.ref_id.apply(make_envelope_link)

    well_cols = [
        "dh_no",
        "unit_hyphen",
        "unit_long",
        "obs_no",
        "dh_name",
        "dh_other_name",
        "aquifer",
        "comments",
        "water_point",
        "water_point_type",
        "easting",
        "northing",
        "zone",
        "latitude",
        "longitude",
        "purpose",
        "pwa",
        "hundred",
        "landscape",
        "owner",
        "drill_method",
        "orig_drilled_depth",
        "orig_drilled_date",
        "max_drilled_depth",
        "max_drilled_depth_date",
        "latest_open_depth",
        "latest_open_depth_date",
        "latest_cased_from",
        "latest_cased_to",
        "latest_casing_min_diam",
        "latest_dtw",
        "latest_swl",
        "latest_rswl",
        "latest_dry",
        "latest_wl_date",
        "latest_ec",
        "latest_tds",
        "latest_sal_date",
        "latest_yield",
        "latest_yield_date",
        "latest_yield_extract_meth",
        "latest_yield_duration",
        "latest_yield_meth",
        "latest_ref_elev",
        "latest_elev_date",
        "state_asset",
        "state_asset_status",
        "state_asset_retained",
        "owner_code",
        "state_asset_comments",
        "engineering_dh",
        "water_well",
        "mineral_dh",
        "petroleum_well",
        "seismic_dh",
        "stratigraphic_dh",
        "survey_horiz_accuracy",
        "survey_horiz_meth",
        "nrm",
        "latest_ph",
        "latest_ph_date",
        "replaced_date",
        "parent_dh_no",
        "child_dh_no",
    ]
    elev_cols = [
        "elev_date",
        "applied_date",
        "ground_elev",
        "ref_elev",
        "ref_height [calculated]",
        "survey_meth",
        "ref_point_type",
        "comments",
        "created_by",
        "creation_date",
        "modified_by",
        "modified_date",
    ]
    notes_cols = [
        "note_no",
        "note_date",
        "author",
        "note",
        "created_by",
        "creation_date",
        "modified_by",
        "modified_date",
    ]
    status_cols = [
        "status_date",
        "status_code",
        "status_desc",
        "created_by",
        "creation_date",
        "modified_by",
        "modified_date",
    ]
    aqmon_cols = [
        "current_aquifer",
        "aquifer_mon_from",
        "aquifer_mon",
        "aquifer_desc",
        "comments",
        "created_by",
        "creation_date",
        "modified_by",
        "modified_date",
    ]
    files_cols = [
        "file_no",
        "file_name",
        "file_type_code",
        "comments",
        "file_doc_type_code",
        "created_by",
        "creation_date",
        "modified_by",
        "modified_date",
    ]
    geophyslogs_cols = [
        "job_no",
        "logged_date",
        "client",
        "purpose",
        "operators",
        "vehicle",
        "max_log_depth",
        "comments",
    ]
    const_cols = [
        "completion_date",
        "event_type",
        "activity",
        "permit_no",
        "wcr_id",
        "driller_name",
        "driller_class",
        "current_depth",
        "drill_method",
        "casing_to",
        "casing_material",
        "casing_min_diam",
        "comments",
        "pzone_type",
        "pzone_from",
        "pzone_to",
    ]
    refs_cols = [
        "info_type",
        "info_title",
        "ref_type",
        "ref_id",
        "ref_title",
        "ref_publication",
    ]

    well["title"] = webapp_utils.make_dh_title(well)
    well_table = webapp_utils.series_to_html(well[well_cols])
    groups_table = webapp_utils.frame_to_html(groups)
    elev_table = webapp_utils.frame_to_html(elev[elev_cols])
    notes_table = webapp_utils.frame_to_html(notes[notes_cols])
    status_table = webapp_utils.frame_to_html(status[status_cols])
    aqmon_table = webapp_utils.frame_to_html(aqmon[aqmon_cols])
    files_table = webapp_utils.frame_to_html(files[files_cols])
    geophyslogs_table = webapp_utils.frame_to_html(geophyslogs[geophyslogs_cols])
    const_table = webapp_utils.frame_to_html(const[const_cols])
    refs_table = webapp_utils.frame_to_html(refs[refs_cols].drop_duplicates())

    return templates.TemplateResponse(
        "well_summary.html",
        {
            "request": request,
            "env": env,
            "title": well.title,
            "redirect_to": "well_summary",
            "singular_redirect_to": "well_summary",
            "plural_redirect_to": "wells_summary",
            "wells_title": "1 well",
            "wells_query_params": "url_str=" + webapp_utils.dhnos_to_urlstr([dh_no]),
            "well": well,
            "groups": groups,
            "elev": elev,
            "notes": notes,
            "status": status,
            "aqmon": aqmon,
            "files": files,
            "const": const,
            "refs": refs,
            "geophyslogs": geophyslogs,
            "well_table": well_table,
            "groups_table": groups_table,
            "elev_table": elev_table,
            "notes_table": notes_table,
            "status_table": status_table,
            "aqmon_table": aqmon_table,
            "files_table": files_table,
            "geophyslogs_table": geophyslogs_table,
            "const_table": const_table,
            "refs_table": refs_table,
        },
    )


@router.get("/well_manual_water_level")
def well_manual_water_level(
    request: Request, dh_no: int, param: str = "swl", env: str = "prod"
) -> str:
    db = connect_to_sageodata(service_name=env)
    df = db.water_levels([dh_no]).sort_values("obs_date", ascending=False)
    well = get_well_metadata(df, dh_no)

    table = webapp_utils.frame_to_html(gd.cleanup_columns(df, keep_cols=[]))

    chart_rows = []
    for idx, record in (
        df.dropna(subset=["swl", "obs_date"], how="any")
        .sort_values("obs_date")
        .iterrows()
    ):
        record = record.to_dict()
        record["js_date"] = record["obs_date"].strftime(f'new Date("%Y/%m/%d")')
        if param in ("dtw", "swl"):
            value = str(record[param] * -1)
        elif param == "rswl":
            value = str(record[param])
        if pd.isnull(value) or value == "NaT" or str(value) == "nan":
            value = "NaN"
        row = "[ " + record["js_date"] + ", " + value + "]"
        chart_rows.append(row)
    chart_data = ",".join(chart_rows)

    return templates.TemplateResponse(
        "well_manual_water_level.html",
        {
            "request": request,
            "env": env,
            "title": well.title,
            "redirect_to": "well_manual_water_level",
            "singular_redirect_to": "well_manual_water_level",
            "plural_redirect_to": "wells_summary",
            "wells_title": "1 well",
            "wells_query_params": "url_str=" + webapp_utils.dhnos_to_urlstr([dh_no]),
            "well": well,
            "df": df,
            "chart_data": chart_data,
            "table": table,
            "param": param,
        },
    )


@router.get("/well_logger_water_level")
def well_logger_water_level(
    request: Request,
    dh_no: int,
    param: str = "swl",
    freq: str = "1d",
    keep_grades: str = "1, 20, 30",
    max_gap_days: float = 1,
    start: str = "",
    finish: str = "",
    env: str = "prod",
    aqts_env: str = "prod",
) -> str:
    if not start:
        start = None
        start_str = ""
    else:
        start = gd.timestamp_acst(start)
        start_str = start.strftime("%Y-%m-%d")

    if not finish:
        finish = None
        finish_str = ""
    else:
        finish = gd.timestamp_acst(finish)
        finish_str = finish.strftime("%Y-%m-%d")

    keep_grades = [int(g) for g in keep_grades.split(",")] if keep_grades else []
    keep_grades_str = ", ".join([f"{g:.0f}" for g in sorted(keep_grades)])

    db = connect_to_sageodata(service_name=env)
    summ = db.wells_summary([dh_no])
    well = get_well_metadata(summ, dh_no)
    aq = gd.DEWAquarius(env=aqts_env)
    dfs = aq.fetch_timeseries_data(
        well.unit_hyphen,
        param=param,
        freq=freq,
        max_gap_days=max_gap_days,
        start=start,
        finish=finish,
        keep_grades=keep_grades,
    )

    chart_rows = []
    df = gd.join_logger_data_intervals(dfs)
    for idx, record in df.iterrows():
        record = record.to_dict()
        record["js_date"] = record["timestamp"].strftime(f'new Date("%Y/%m/%d %H:%M")')
        if param in ("dtw", "swl"):
            value = str(record[param] * -1)
        elif param == "rswl":
            value = str(record[param])
        if pd.isnull(value) or value == "NaT" or str(value) == "nan":
            value = "NaN"
        row = "[ " + record["js_date"] + ", " + value + "]"
        chart_rows.append(row + "\n")
    chart_data = ",".join(chart_rows)

    download_url = (
        f"/api/well_best_available_logger_data"
        f"?unit_hyphen={well.unit_hyphen}"
        f"&param={param}"
        f"&freq={freq}"
        f"&keep_grades={keep_grades_str}"
        f"&max_gap_days={int(max_gap_days)}"
        f"&start={start_str}"
        f"&finish={finish_str}"
        f"&aqts_env={aqts_env}"
        f"&format=csv"
    )

    dsets = gd.get_logger_interval_details(dfs)
    dsets["csv_download"] = dsets.apply(
        lambda row: (
            f"<a href='"
            f"/api/well_best_available_logger_data"
            f"?unit_hyphen={well.unit_hyphen}"
            f"&param={param}"
            f"&freq={freq}"
            f"&keep_grades={keep_grades_str}"
            f"&max_gap_days={int(max_gap_days)}"
            f"&start={row.start_timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
            f"&finish={row.finish_timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
            f"&aqts_env={aqts_env}"
            f"&format=csv"
            f"'>{row.dataset_length}-row CSV</a>"
        ),
        axis=1,
    )
    dsets_table = webapp_utils.frame_to_html(dsets)

    return templates.TemplateResponse(
        "well_logger_water_level.html",
        {
            "request": request,
            "env": env,
            "aqts_env": aqts_env,
            "title": well.title,
            "redirect_to": "well_logger_water_level",
            "singular_redirect_to": "well_logger_water_level",
            "plural_redirect_to": "wells_summary",
            "wells_title": "1 well",
            "wells_query_params": "url_str=" + webapp_utils.dhnos_to_urlstr([dh_no]),
            "well": well,
            "chart_data": chart_data,
            "start": start_str,
            "finish": finish_str,
            "freq": freq,
            "max_gap_days": max_gap_days,
            "param": param,
            "keep_grades": keep_grades_str,
            "dsets_table": dsets_table,
            "download_url": download_url,
        },
    )


@router.get("/well_combined_water_level")
def well_combined_water_level(
    request: Request,
    dh_no: int,
    param: str = "swl",
    freq: str = "1d",
    keep_grades: str = "1, 20, 30",
    max_gap_days: float = 550,
    start: str = "",
    finish: str = "",
    env: str = "prod",
    aqts_env: str = "prod",
) -> str:
    if not start:
        start = None
        start_str = ""
    else:
        start = gd.timestamp_acst(start)
        start_str = start.strftime("%Y-%m-%d")

    if not finish:
        finish = None
        finish_str = ""
    else:
        finish = gd.timestamp_acst(finish)
        finish_str = finish.strftime("%Y-%m-%d")

    keep_grades = [int(g) for g in keep_grades.split(",")] if keep_grades else []
    keep_grades_str = ", ".join([f"{g:.0f}" for g in sorted(keep_grades)])

    db = connect_to_sageodata(service_name=env)
    summ = db.wells_summary([dh_no])
    well = get_well_metadata(summ, dh_no)

    dfs = gd.get_combined_water_level_dataset(
        [well.dh_no],
        db=db,
        param=param,
        freq=freq,
        start=start,
        finish=finish,
        max_gap_days=max_gap_days,
        keep_grades=keep_grades,
        aq_env=aqts_env,
    )
    df = gd.join_logger_data_intervals(dfs)

    chart_rows = []
    chart_columns = [c for c in [f"{param}-SAGD", f"{param}-AQTS", param] if c in df]
    for idx, record in df.iterrows():
        record = record.to_dict()
        row_str = "[ " + record["timestamp"].strftime(f'new Date("%Y/%m/%d %H:%M")')
        for column in chart_columns:
            value = record[column]
            if not str(value) in ("null", "NaN", "NaT"):
                if column.startswith("rswl"):
                    value = f"{value:.3f}"
                else:
                    value = f"{value * -1:.3f}"

            if value in ("NaT", "NaN", "nan"):
                value = "NaN"
            elif value == "null":
                # important to keep "null" - used by dygraphs
                pass
            else:
                # numerical value has been encoded.
                pass

            row_str += f", {value}"
        row_str += "]"
        chart_rows.append(row_str + "\n")
    chart_data = ",".join(chart_rows)
    chart_columns_str = ", ".join([f'"{col}"' for col in chart_columns])

    url_str = webapp_utils.dhnos_to_urlstr([dh_no])

    download_url = (
        f"/api/well_best_available_combined_water_level_data"
        f"?url_str={url_str}"
        f"&param={param}"
        f"&freq={freq}"
        f"&keep_grades={keep_grades_str}"
        f"&max_gap_days={int(max_gap_days)}"
        f"&start={start_str}"
        f"&finish={finish_str}"
        f"&env={env}"
        f"&aqts_env={aqts_env}"
        f"&format=csv"
    )
    dsets = gd.get_logger_interval_details(dfs)
    if len(dsets):
        dsets["csv_download"] = dsets.apply(
            lambda row: (
                f"<a href='"
                f"/api/well_best_available_combined_water_level_data"
                f"?url_str={url_str}"
                f"&param={param}"
                f"&freq={freq}"
                f"&keep_grades={keep_grades_str}"
                f"&max_gap_days={int(max_gap_days)}"
                f"&start={row.start_timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
                f"&finish={row.finish_timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
                f"&env={env}"
                f"&aqts_env={aqts_env}"
                f"&format=csv"
                f"'>{row.dataset_length}-row CSV</a>"
            ),
            axis=1,
        )
    dsets_table = webapp_utils.frame_to_html(dsets)

    return templates.TemplateResponse(
        "well_combined_water_level.html",
        {
            "request": request,
            "env": env,
            "aqts_env": aqts_env,
            "title": well.title,
            "redirect_to": "well_combined_water_level",
            "singular_redirect_to": "well_combined_water_level",
            "plural_redirect_to": "wells_summary",
            "wells_title": "1 well",
            "wells_query_params": f"url_str={url_str}",
            "well": well,
            "chart_data": chart_data,
            "chart_columns_str": chart_columns_str,
            "start": start_str,
            "finish": finish_str,
            "freq": freq,
            "max_gap_days": max_gap_days,
            "param": param,
            "keep_grades": keep_grades_str,
            "dsets_table": dsets_table,
            "download_url": download_url,
        },
    )


@router.get("/well_salinity")
def well_salinity(request: Request, dh_no: int, env: str = "prod") -> str:
    db = connect_to_sageodata(service_name=env)
    df = db.salinities([dh_no]).sort_values("collected_date", ascending=False)
    well = get_well_metadata(df, dh_no)
    table = webapp_utils.frame_to_html(
        gd.cleanup_columns(df, keep_cols=[]).drop(
            ["amg_easting", "amg_northing"], axis=1
        )
    )

    chart_rows = []
    for idx, record in (
        df.dropna(subset=["ec", "collected_date"], how="any")
        .sort_values("collected_date")
        .iterrows()
    ):
        record = record.to_dict()
        record["js_date"] = record["collected_date"].strftime(f'new Date("%Y/%m/%d")')
        row = (
            "[ "
            + record["js_date"]
            + ", "
            + str(record["ec"])
            + ", "
            + str(record["tds"])
            + "]"
        )
        chart_rows.append(row)
    chart_data = ",".join(chart_rows)

    return templates.TemplateResponse(
        "well_salinity.html",
        {
            "request": request,
            "env": env,
            "title": well.title,
            "redirect_to": "well_salinity",
            "singular_redirect_to": "well_salinity",
            "plural_redirect_to": "wells_summary",
            "wells_title": "1 well",
            "wells_query_params": "url_str=" + webapp_utils.dhnos_to_urlstr([dh_no]),
            "well": well,
            "df": df,
            "chart_data": chart_data,
            "table": table,
        },
    )


@router.get("/well_drillhole_logs")
def well_drillhole_logs(request: Request, dh_no: int, env: str = "prod") -> str:
    db = connect_to_sageodata(service_name=env)

    logs = db.drillhole_logs([dh_no]).sort_values("log_date", ascending=True)
    log_types = logs.log_type.unique()

    drill = db.drillers_logs([dh_no]).sort_values(["depth_from", "depth_to"])
    lith = db.lith_logs([dh_no]).sort_values(["depth_from", "depth_to"])
    strat = db.strat_logs([dh_no]).sort_values(["depth_from", "depth_to"])
    hstrat = db.hydrostrat_logs([dh_no])  # .sort_values(["depth_from", "depth_to"])

    well = get_well_metadata(logs, dh_no)

    logs_table = webapp_utils.frame_to_html(gd.cleanup_columns(logs, keep_cols=[]))
    drill_table = webapp_utils.frame_to_html(gd.cleanup_columns(drill, keep_cols=[]))
    lith_table = webapp_utils.frame_to_html(gd.cleanup_columns(lith, keep_cols=[]))
    strat_table = webapp_utils.frame_to_html(gd.cleanup_columns(strat, keep_cols=[]))
    hstrat_table = webapp_utils.frame_to_html(gd.cleanup_columns(hstrat, keep_cols=[]))

    return templates.TemplateResponse(
        "well_drillhole_logs.html",
        {
            "request": request,
            "env": env,
            "title": well.title,
            "redirect_to": "well_drillhole_logs",
            "singular_redirect_to": "well_drillhole_logs",
            "plural_redirect_to": "wells_summary",
            "wells_title": "1 well",
            "wells_query_params": "url_str=" + webapp_utils.dhnos_to_urlstr([dh_no]),
            "well": well,
            "logs": logs,
            "log_types": log_types,
            "drill": drill,
            "lith": lith,
            "strat": strat,
            "hstrat": hstrat,
            "logs_table": logs_table,
            "drill_table": drill_table,
            "lith_table": lith_table,
            "strat_table": strat_table,
            "hstrat_table": hstrat_table,
        },
    )


@router.get("/well_construction")
def well_construction(request: Request, dh_no: int, env: str = "prod") -> str:
    db = connect_to_sageodata(service_name=env)

    cevents_df = db.construction_events([dh_no]).sort_values(
        "completion_date", ascending=False
    )

    well = get_well_metadata(cevents_df, dh_no)

    cevents_df = gd.add_construction_activity_column(cevents_df)
    summary_cols = [
        "completion_date",
        "event_type",
        "activity",
        "wcr_id",
        "driller_name",
        "driller_class",
        "permit_no",
        "comments",
        "total_depth",
        "final_depth",
        "current_depth",
        "final_swl",
        "final_yield",
        "drill_method",
        "drill_to",
        "casing_material",
        "casing_min_diam",
        "casing_to",
        "pzone_type",
        "pzone_material",
        "pzone_diam",
        "pzone_from",
        "pzone_to",
    ]
    summary_table = webapp_utils.frame_to_html(
        gd.cleanup_columns(cevents_df[summary_cols], keep_cols=[])
    )

    # drilling, casing, wcuts, pzones, other_items
    drilling = db.drilled_intervals([dh_no]).sort_values(["depth_from", "depth_to"])
    casing = db.casing_strings([dh_no]).sort_values(["depth_from", "depth_to"])
    seals = db.casing_seals([dh_no]).sort_values("seal_depth")
    wcuts = db.water_cuts([dh_no]).sort_values(["depth_from", "depth_to"])
    pzones = db.production_zones([dh_no]).sort_values(["depth_from", "depth_to"])
    other_items = db.other_construction_items([dh_no]).sort_values(
        ["depth_from", "depth_to"]
    )

    elev = (
        db.elevation_surveys([dh_no])
        .pipe(gd.cleanup_columns)
        .assign(**{"ref_height [calculated]": pd.NA})
    )
    elev.loc[
        (~pd.isnull(elev.ground_elev)) & (~pd.isnull(elev.ref_elev)),
        "ref_height [calculated]",
    ] = (
        elev.ref_elev - elev.ground_elev
    )
    elev_cols = [
        "elev_date",
        "applied_date",
        "ground_elev",
        "ref_elev",
        "ref_height [calculated]",
        "survey_meth",
        "ref_point_type",
        "comments",
    ]
    elev = elev[elev_cols]

    cevents = []
    sevents = []

    kws = dict(
        keep_cols=[],
        drop=("construction_aquifer", "completion_no", "completion_date", "event_type"),
    )

    for completion_no, cevent_summ in cevents_df.groupby("completion_no"):
        summary = gd.cleanup_columns(cevent_summ, keep_cols=[]).iloc[0]
        if summary.event_type == "C":
            title = f"Construction event "
        elif summary.event_type == "S":
            title = f"Survey event "
        title += webapp_utils.format_datetime(summary.completion_date)

        summary = summary.drop(
            [
                "latest",
                "max_case",
                "orig_case",
                "lod_case",
                "from_flag",
            ]
        )
        summary_1_cols = [
            "commenced_date",
            "completion_date",
            "completion_no",
            "event_type",
            "activity",
            "wcr_id",
            "permit_no_full",
            "driller_name",
            "driller_class",
            "plant_operator",
            "construction_aquifer",
            "total_depth",
            "final_depth",
            "current_depth",
            # "start_depth",
        ]
        summary_2_cols = [
            "drill_method",
            "drill_from",
            "drill_to",
            "drill_diam",
            "casing_material",
            "casing_from",
            "casing_to",
            "casing_diam",
            "casing_min_diam",
            "pzone_type",
            "pzone_material",
            "pzone_from",
            "pzone_to",
            "pzone_diam",
            "pcement_from",
            "pcement_to",
            "created_by",
            "creation_date",
            "modified_by",
            "modified_date",
        ]

        summary_1 = summary[summary_1_cols]
        summary_2 = summary[summary_2_cols]
        summary_12 = summary[summary_1_cols + summary_2_cols]

        cevent = {
            "data_types": [],
            "title": title,
            "summary": summary,
            "summary_1": summary_1,
            "summary_2": summary_2,
            "summary_12": summary_12,
            "comments": summary.comments,
            "summary_table": webapp_utils.series_to_html(
                summary.drop(index=["comments"]), transpose=False
            ),
            "summary_1_table": webapp_utils.series_to_html(summary_1, transpose=False),
            "summary_2_table": webapp_utils.series_to_html(summary_2, transpose=False),
            "summary_12_table": webapp_utils.series_to_html(summary_12, transpose=True),
        }

        cevent_drilling = drilling[drilling.completion_no == completion_no]
        if len(cevent_drilling) > 0:
            cevent["drilling"] = webapp_utils.frame_to_html(
                gd.cleanup_columns(cevent_drilling, **kws)
            )
            cevent["data_types"].append("drilling")

        cevent_casing = casing[casing.completion_no == completion_no]
        if len(cevent_casing) > 0:
            cevent["casing"] = webapp_utils.frame_to_html(
                gd.cleanup_columns(cevent_casing, **kws)
            )
            cevent["data_types"].append("casing")

        cevent_seals = seals[seals.completion_no == completion_no]
        if len(cevent_seals) > 0:
            cevent["seals"] = webapp_utils.frame_to_html(
                gd.cleanup_columns(cevent_seals, **kws)
            )
            cevent["data_types"].append("seals")

        cevent_wcuts = wcuts[wcuts.completion_no == completion_no]
        if len(cevent_wcuts) > 0:
            cevent["wcuts"] = webapp_utils.frame_to_html(
                gd.cleanup_columns(cevent_wcuts, **kws)
            )
            cevent["data_types"].append("wcuts")

        cevent_pzones = pzones[pzones.completion_no == completion_no]
        if len(cevent_pzones) > 0:
            cevent["pzones"] = webapp_utils.frame_to_html(
                gd.cleanup_columns(
                    cevent_pzones.drop(["pzone_from", "pzone_to"], axis=1), **kws
                )
            )
            cevent["data_types"].append("pzones")

        cevent_other_items = other_items[other_items.completion_no == completion_no]
        if len(cevent_other_items) > 0:
            cevent["other_items"] = webapp_utils.frame_to_html(
                gd.cleanup_columns(cevent_other_items, **kws)
            )
            cevent["data_types"].append("other_items")

        if summary.event_type == "C":
            cevents.append(cevent)
        elif summary.event_type == "S":
            sevents.append(cevent)

    cevents = sorted(cevents, key=lambda x: x["summary"].completion_date)
    sevents = sorted(sevents, key=lambda x: x["summary"].completion_date)
    elev_table = webapp_utils.frame_to_html(elev)

    return templates.TemplateResponse(
        "well_construction.html",
        {
            "request": request,
            "env": env,
            "title": well.title,
            "redirect_to": "well_construction",
            "singular_redirect_to": "well_construction",
            "plural_redirect_to": "wells_summary",
            "wells_title": "1 well",
            "wells_query_params": "url_str=" + webapp_utils.dhnos_to_urlstr([dh_no]),
            "well": well,
            "summary_table": summary_table,
            "events": [cevents, sevents],
            "elev": elev,
            "elev_table": elev_table,
        },
    )


@router.get("/well_drillhole_document_images")
def well_drillhole_document_images(
    request: Request,
    dh_no: int,
    env: str = "prod",
    width: int = 950,
    height: int = -1,
    inline: bool = False,
    new_tab: bool = False,
) -> str:
    db = connect_to_sageodata(service_name=env)
    df = db.drillhole_document_image_list([dh_no])
    well = get_well_metadata(df, dh_no)

    images = [im for idx, im in df.iterrows()]

    return templates.TemplateResponse(
        "well_drillhole_document_images.html",
        {
            "request": request,
            "env": env,
            "title": well.title,
            "redirect_to": "well_drillhole_document_images",
            "singular_redirect_to": "well_drillhole_document_images",
            "plural_redirect_to": "wells_summary",
            "wells_title": "1 well",
            "wells_query_params": "url_str=" + webapp_utils.dhnos_to_urlstr([dh_no]),
            "well": well,
            "df": df,
            "images": images,
            "width": width,
            "height": height,
            "inline": inline,
            "new_tab": new_tab,
            "target": "_blank" if new_tab else "",
        },
    )


@router.get("/well_geophysical_logs")
def well_geophysical_logs(
    request: Request,
    dh_no: int,
    env: str = "prod",
) -> str:
    db = connect_to_sageodata(service_name=env)
    md = db.geophys_log_metadata([dh_no])
    job_nos = md.job_no.unique()
    files = gd.list_geophys_job_files(job_nos=job_nos, add_las_metadata=True)
    well = get_well_metadata(md, dh_no)

    md_lookup = md.set_index("job_no").logged_date
    files.insert(1, "logged_date", files.job_no.map(md_lookup))

    files_tables = []
    job_row_cols = [
        "log_hdr_no",
        "project",
        "client",
        "location",
        "purpose",
        "operators",
        "vehicle",
        "gl_dh_name",
        "gl_permit_no",
        "max_log_depth",
        "comments",
    ]

    def link_log_types(row):
        log_types = [lt.strip() for lt in row.log_types.split(",")]
        links = []
        for log_type in log_types:
            links.append(
                f"<a href='/app/well_geophysical_log_las_file?job_no={row.job_no}&filename={row.filename}&log_type={log_type}'>{log_type}</a>"
            )
        links.append(
            f"<a href='/app/well_geophysical_log_las_file?job_no={row.job_no}&filename={row.filename}'>[all log type curves]</a>"
        )
        return ", ".join(links)

    def link_log_mnemonics(row):
        mnemonics = [m.strip() for m in row.mnemonics.split(",")]
        links = []
        for mnemonic in mnemonics:
            links.append(
                f"<a href='/app/well_geophysical_log_las_file?job_no={row.job_no}&filename={row.filename}&mnemonic={mnemonic}'>{mnemonic}</a>"
            )
        links.append(
            f"<a href='/app/well_geophysical_log_las_file?job_no={row.job_no}&filename={row.filename}'>[all curves]</a>"
        )
        return ", ".join(links)

    for (logged_date, job_no), job_files in files.groupby(
        ["logged_date", "job_no"], as_index=False
    ):
        job_files.loc[job_files.file_type == "LAS", "log_types"] = job_files.apply(
            link_log_types, axis=1
        )
        job_files.loc[job_files.file_type == "LAS", "mnemonics"] = job_files.apply(
            link_log_mnemonics, axis=1
        )
        job_files["filename"] = job_files.filename.apply(
            lambda filename: f"<a href='/api/well_geophysical_log_file?job_no={job_no}&filename={filename}'>{filename}</a>"
        )
        files_table = webapp_utils.frame_to_html(
            gd.cleanup_columns(job_files, drop=["path"], keep_cols=[])
        )
        md_row_table = webapp_utils.series_to_html(
            md.loc[md.job_no == job_no, job_row_cols].iloc[0],
            transpose=False,
        )

        files_tables.append(
            [job_no, logged_date.strftime("%d/%m/%Y"), md_row_table, files_table]
        )

    md["job_no"] = md.job_no.apply(lambda j: f"<a href='#{j}'>{j}</a>")

    md_cols = [
        "job_no",
        "log_hdr_no",
        "logged_date",
        "project",
        "client",
        "location",
        "purpose",
        "operators",
        "vehicle",
        "max_log_depth",
        "comments",
    ]
    md_table = webapp_utils.frame_to_html(gd.cleanup_columns(md, keep_cols=[])[md_cols])

    return templates.TemplateResponse(
        "well_geophysical_logs.html",
        {
            "request": request,
            "env": env,
            "title": well.title,
            "redirect_to": "well_geophysical_logs",
            "singular_redirect_to": "well_geophysical_logs",
            "plural_redirect_to": "wells_summary",
            "wells_title": "1 well",
            "wells_query_params": "url_str=" + webapp_utils.dhnos_to_urlstr([dh_no]),
            "well": well,
            "md": md,
            "files": files,
            "md_table": md_table,
            "files_tables": files_tables,
        },
    )


@router.get("/well_geophysical_log_las_file")
def well_geophysical_log_las_file(
    request: Request,
    job_no: int,
    filename: str,
    log_type: str = "",
    mnemonic: str = "",
    env: str = "prod",
) -> str:
    db = connect_to_sageodata(service_name=env)
    job_path = gd.find_job_folder(job_no)
    file_path = job_path / filename

    md = db.geophys_log_metadata_by_job_no([job_no])
    dh_no = md.dh_no.iloc[0]
    well = get_well_metadata(md, dh_no)

    import pozo

    las = lasio.read(file_path)
    las_md = gd.get_las_metadata(las=las)

    if log_type:
        include_mnemonics = [
            m["las_mnemonic"] for m in las_md["mnemonics"] if m["log_type"] == log_type
        ]
    elif mnemonic:
        include_mnemonics = [
            m["las_mnemonic"]
            for m in las_md["mnemonics"]
            if m["las_mnemonic"] == mnemonic
        ]
    else:
        include_mnemonics = [
            m["las_mnemonic"] for m in las_md["mnemonics"] if m["log_type"] != "?"
        ]
    graph = pozo.Graph(las, include=include_mnemonics)

    fig_html = graph.render(height=750).to_html(full_html=False, include_plotlyjs=True)

    return templates.TemplateResponse(
        "well_geophysical_log_las_file.html",
        {
            "request": request,
            "env": env,
            "title": well.title,
            "redirect_to": "well_geophysical_logs",
            "singular_redirect_to": "well_geophysical_logs",
            "plural_redirect_to": "wells_summary",
            "wells_title": "1 well",
            "wells_query_params": "url_str=" + webapp_utils.dhnos_to_urlstr([dh_no]),
            "well": well,
            "fig_html": fig_html,
        },
    )
