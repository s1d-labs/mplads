"""Pure functions on the dashboard's answer."""
import json


def body(state, house, tenure, report):
    return {"combo": f"{state},0,0,{house},{tenure}", "key": report}


def rows(answer):
    """The answer holds one field with a list, sometimes as a JSON string. Only rows with Sno are data."""
    if not answer:
        return []
    r = answer[list(answer)[0]]
    r = json.loads(r) if isinstance(r, str) else r
    return [x for x in r if isinstance(x, dict) and "Sno" in x]


def record_id(tag, state, report, row):
    return f"{tag}-{state}-{report.split()[0].lower()}-{row.get('WORK_RECOMMENDATION_DTL_ID', '')}-{row.get('Sno')}"
