# InternShield

InternShield is a student-focused internship risk assessment demo. It scans advertisement text and user-provided details for configured warning signs, explains triggered rules, and offers safety recommendations.

## Stack
- Python 3.10+
- Flask
- HTML, CSS, JavaScript
- Rule-based text analysis
- pytest

## Run locally

### Windows (PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation, run the commands below without activating the environment:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Test
```bash
python -m pytest -q
```

## API
`POST /api/analyze` accepts JSON with:
- `description` (required)
- `company_name`
- `company_website`
- `recruiter_email`
- `stipend`
- `payment_requested` (boolean)

`GET /api/samples` returns demo sample offers.

## Important limitations
- The scoring weights and keyword patterns are illustrative heuristics, not a validated fraud model.
- The score is not a probability of fraud.
- The app does not verify company registration, website ownership, recruiter identity, or live domain reputation.
- A domain mismatch can occur for legitimate third-party recruiters and should only be treated as a signal to check.
- A low score does not prove an offer is genuine; a high score does not prove fraud.
- This demo does not save scans in a database. Avoid pasting personal or sensitive information.
- Do not deploy the Flask development server with debug mode enabled to a public production environment.

## Suggested next improvements
- Expand negation/context handling and add a larger set of labeled test cases.
- Evaluate the rules against a representative, legally usable dataset.
- Add optional verified external data sources with clear provenance and failure handling.
- Consider a trained classifier only after suitable data and evaluation are available.
