"""One dashboard report: one record per row, and the raw answer in the bucket."""
import gzip
import os
import sys
import time

import requests
from scrape_hub_client import HubClient, stop_flag, timed_post

from parse import body, record_id, rows

PROJECT = os.environ["SCRAPE_POOL_PROJECT"]
DEADLINE = time.time() + float(os.environ.get("SCRAPE_MAX_HOURS", "1")) * 3600 - 120
URL = "https://mplads.mospi.gov.in/rest/PreLoginDashboardData/getTilesReportData"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
HEADERS = {"Content-Type": "application/json; charset=utf-8", "Accept": "application/json, text/javascript, */*; q=0.01", "X-Requested-With": "XMLHttpRequest", "Referer": "https://mplads.mospi.gov.in/digigov/dashboard.html", "Origin": "https://mplads.mospi.gov.in", "User-Agent": UA, "X-Client-UA": UA}
stop = stop_flag(install=False)     # set on SIGINT / SIGTERM once main() installs the handlers


def main():
    hub = HubClient(PROJECT, job_index=int(os.environ.get("SCRAPE_JOB_INDEX", 0)), total_jobs=int(os.environ.get("SCRAPE_TOTAL_JOBS", 1)))
    stop_flag()
    s = requests.Session()
    s.headers.update(HEADERS)
    while time.time() < DEADLINE and not stop.is_set():
        if hub.settings.get("paused"):
            time.sleep(30)
            continue
        items = hub.claim(1, steal=True, retry_failed=True)
        if not items:
            break
        it = items[0]
        p = it["payload"]
        r = timed_post(hub, s, URL, json=body(p["state"], p["house"], p["tenure"], p["report"]), timeout=(20, 180))  # request metrics
        if r is None:
            hub.complete([it["key"]], "failed", error="no answer")
            continue
        if r.status_code != 200:
            hub.complete([it["key"]], "failed", error=f"http {r.status_code}")
            continue
        got = rows(r.json())
        for row in got:
            hub.record(record_id(p["tag"], p["state"], p["report"], row), {"state": p["state"], "term": p["tag"], "report": p["report"], **row})
        if got:
            hub.upload_many([(f"raw/{it['key']}.json.gz", gzip.compress(r.content), "application/gzip")])
        hub.complete([it["key"]], "done", fetched=len(got))
        time.sleep(max(1, hub.settings.get("delay_ms", 0) / 1000))
    hub.close("finished" if not stop.is_set() else "failed", "" if not stop.is_set() else "stopped by signal")


if __name__ == "__main__":
    sys.exit(main())
