# mplads: works by Members of Parliament

A family of the s1d-labs scrape pool. It reads the public dashboard reports of mplads.mospi.gov.in: works recommended, sanctioned, completed and the spending on them,
for every state, the 17th and 18th Lok Sabha and the Rajya Sabha. One record per report row. The raw answers are in the bucket under `raw/`.

- Only the calls that the public dashboard makes. No login, captcha or OTP.
- Runs on the India servers (`geo="IN"`), 2 workers, one request every 1.5 seconds.

Setup: change `family.py`, then Actions -> setup. Tests: `python -m pytest tests`.
