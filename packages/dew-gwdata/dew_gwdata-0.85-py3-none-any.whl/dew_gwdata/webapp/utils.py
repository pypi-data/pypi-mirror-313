import pandas as pd


def make_dh_title(well, elements=("unit_no", "obs_no", "dh_name")):
    data = dict(
        dh_no=f"DH {well.dh_no}",
        unit_no=str(well.unit_hyphen).replace("None", ""),
        obs_no=str(well.obs_no).replace("None", ""),
        dh_name=str(well.dh_name).replace("None", ""),
        aquifer=str(well.aquifer).replace("None", ""),
    )
    components = [data[x] for x in elements]
    valid_components = [c for c in components if c]
    if len(valid_components) == 0:
        valid_components = [data["dh_no"]]
    title = " / ".join(valid_components)
    if data["aquifer"]:
        title += f" ({data['aquifer']})"
    return title


def format_datetime(dt):
    try:
        tstamp = pd.Timestamp(dt)
    except:
        return dt
    else:
        if pd.isnull(tstamp):
            return ""
        else:
            if tstamp.hour == tstamp.minute == tstamp.second == 0:
                return tstamp.strftime("%d/%m/%Y")
            else:
                return tstamp.strftime("%d/%m/%Y %H:%M:%S")


def frame_to_html(
    df,
    transpose_last=False,
    apply=None,
    apply_kws=None,
    remove_col_underscores=True,
    bold_rows=False,
    **kwargs,
):
    if apply_kws is None:
        apply_kws = {}
    if remove_col_underscores:
        df.columns = [str(c).replace("_", " ") for c in df.columns]
    for col in df.columns:
        if "date" in col:
            df[col] = df[col].apply(lambda v: f"<nobr>{format_datetime(v)}</nobr>")
        if col in ("unit hyphen", "unit no"):
            df[col] = df[col].apply(lambda v: f"<nobr>{v}</nobr>")
    df = df.fillna("")
    kwargs["escape"] = False
    if transpose_last:
        df = df.T
    df = df.map(lambda s: s.replace("\n", "<br />") if isinstance(s, str) else s)
    if apply is None:
        table_html = df.to_html(classes="", bold_rows=bold_rows, **kwargs)
    else:
        if "subset" in apply_kws:
            apply_kws["subset"] = [col.replace("_", " ") for col in apply_kws["subset"]]

        styler = df.style.apply(apply, **apply_kws)
        table_html = styler.to_html(bold_rows=bold_rows)
    return "<div class='table-outer-wrapper'>" + table_html + "</div>"


def series_to_html(s, transpose=True, **kwargs):
    assert isinstance(s, pd.Series)
    df = s.to_frame()
    if transpose:
        df = df.T
    return frame_to_html(df, transpose_last=True, **kwargs)


import numpy as np

BASE_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-~_"


def to_deltas(arr):
    arr = np.asarray(arr)
    arr = np.sort(arr)
    return np.diff(arr, prepend=0)


def from_deltas(arr):
    return np.cumsum(arr)


def encode(n, characters):
    base = len(characters)
    result = []
    i = 0
    while n > 0:
        i += 1
        quotient = n // base
        remainder = n % base
        result.append(characters[remainder])
        n = quotient
    encoded = "".join(result[::-1])
    return encoded


def decode(s, characters):
    base = len(characters)
    n = 0
    for i, char in enumerate(s[::-1]):
        n += (base**i) * characters.index(char)
    return n


def dhnos_to_urlstr(dh_nos):
    deltas = to_deltas(dh_nos)
    encoded = [encode(d, BASE_CHARS) for d in deltas]
    return ".".join(encoded)


def urlstr_to_dhnos(url_str):
    decoded = [decode(s, BASE_CHARS) for s in url_str.split(".")]
    return from_deltas(decoded)
