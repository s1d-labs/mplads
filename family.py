"""What this family scrapes: the public MPLADS dashboard reports, for every state, house and term.

One queue item = one report for one state. The combo is state,constituency,mp,house,tenure. House 2 = Lok Sabha (tenure 5 = 17th, 7 = 18th),
house 1 = Rajya Sabha (tenure 1 = sitting, 2 = retired). A state number with no data gives an empty report.
"""
import json
from pathlib import Path

FAMILY = json.loads((Path(__file__).parent / "scrape.json").read_text())["family"]
HOST = "mplads.mospi.gov.in"
TERMS = [(2, 5, "ls17"), (2, 7, "ls18"), (1, 1, "rs-sitting"), (1, 2, "rs-retired")]
REPORTS = ["Works Recommended", "Works Sanctioned", "Works Completed", "Expenditure on Completed and On-going Works as on Date"]
STATES = range(1, 41)

PROJECTS = [{"name": f"{FAMILY}-works", "title": "MPLADS works", "task": "tiles", "unit_label": "report", "record_label": "work row",
             "items": [{"key": f"s{s}-{tag}-{r.split()[0].lower()}-{r.split()[1].lower()}", "payload": {"state": s, "house": h, "tenure": t, "tag": tag, "report": r}}
                       for s in STATES for h, t, tag in TERMS for r in REPORTS]}]
PROBES = [{"name": f"{FAMILY}:{HOST}", "url": f"https://{HOST}/digigov/dashboard.html", "expect": "MPLADS"}]
