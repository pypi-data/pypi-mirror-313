from __future__ import annotations

import json


def build_data_preview(preview: list[dict] | None = None, rows_count: int | None = None) -> dict:
    """
    Build data preview.

    Parameters
    ----------
    preview : list[dict] | None
        Preview.
    rows_count : int | None
        Row count.

    Returns
    -------
    dict
        Data preview.
    """
    dict_ = {}
    if preview is not None:
        dict_["cols"] = preview
    if rows_count is not None:
        dict_["rows"] = rows_count
    return dict_


def get_data_preview(columns: list, data: list[list], columnar: bool = False) -> list[dict]:
    """
    Prepare preview.

    Parameters
    ----------
    columns : list
        Columns names.
    data : list[list]
        Data to preview.
    columnar : bool
        If data are arranged in columns. If False, data are arranged in rows.

    Returns
    -------
    list[dict]
        Data preview.
    """
    # Reduce data to 10 rows
    if not columnar:
        if len(data) > 10:
            data = data[:10]
    else:
        data = [d[:10] for d in data]

    # Transpose data if needed
    if not columnar:
        data = list(map(list, list(zip(*data))))

    # Prepare the preview
    data_dict = prepare_preview(columns, data)

    # Filter memoryview values
    filtered_memview = filter_memoryview(data_dict)

    # Check the size of the preview data
    return check_preview_size(filtered_memview)


def prepare_preview(column_names: list, data: list[list]) -> list[dict]:
    """
    Get preview.

    Parameters
    ----------
    data : pd.DataFrame
        Data.

    Returns
    -------
    list[dict]
        Preview.
    """
    if len(column_names) != len(data):
        raise ValueError("Column names and data must have the same length")
    return [{"name": column, "value": values} for column, values in zip(column_names, data)]


def filter_memoryview(data: list[dict]) -> list[dict]:
    """
    Find memoryview values.

    Parameters
    ----------
    data : pd.DataFrame
        Data.

    Returns
    -------
    list[str]
        Column to filter out from preview.
    """
    key_to_filter = []
    for i in data:
        if any(isinstance(v, memoryview) for v in i["value"]):
            key_to_filter.append(i["name"])
    for i in key_to_filter:
        data = [d for d in data if d["name"] != i]
    return data


def check_preview_size(preview: list[dict]) -> list:
    """
    Check preview size. If it's too big, return empty list.

    Parameters
    ----------
    preview : list[dict]
        Preview.

    Returns
    -------
    list
        Preview.
    """
    if len(json.dumps(preview).encode("utf-8")) >= 64000:
        return []
    return preview
