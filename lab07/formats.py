import json


def csv_to_records(text):
    lines = [line.rstrip("\r") for line in text.split("\n")]
    lines = [line for line in lines if line.strip() != ""]
    if not lines:
        return []
    header = [name.strip() for name in lines[0].split(",")]
    records = []
    for line in lines[1:]:
        values = [value.strip() for value in line.split(",")]
        records.append(dict(zip(header, values)))
    return records


def _convert(value):
    lowered = value.lower()
    if lowered in ("true", "yes"):
        return True
    if lowered in ("false", "no"):
        return False
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value.replace(",", "."))
    except ValueError:
        pass
    return value


def parse_settings(lines):
    result = {}
    current_list = None
    for raw in lines:
        line = raw.split("#", 1)[0].rstrip()
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("-"):
            if current_list is not None:
                current_list.append(_convert(stripped[1:].strip()))
            continue
        key, sep, value = stripped.partition(":")
        if not sep:
            continue
        key = key.strip()
        value = value.strip()
        if value == "":
            current_list = []
            result[key] = current_list
        else:
            current_list = None
            result[key] = _convert(value)
    return result


def merge_by_key(rows, extra, key="id"):
    merged = []
    for row in rows:
        info = extra.get(row.get(key))
        if isinstance(info, dict):
            merged.append({**info, **row})
        else:
            merged.append(dict(row))
    return merged


def records_to_json(records):
    return json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True)