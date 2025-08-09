# ReaperScanner AI (MVP)

**AI-assisted web security scanner** — a modular, open-source starter that blends ideas from Burp Suite (intercepting proxy), Acunetix (crawler + checks), and Nessus (reporting), with an **integrated GPT assistant** that can analyze HTTP traffic and teach you how/why a vulnerability might exist.

> This is a minimal but extensible **MVP** you can push to GitHub and grow into a full tool. It ships with:
- **Intercepting proxy** (mitmproxy addon) that streams flows into the pipeline.
- **Async crawler** for site discovery.
- **Detector plugins** (XSS, LFI/RFI, File Upload heuristics, SQLi patterns) as examples.
- **AI Advisor**: routes requests/responses to a chat model when you click *"Analyze with GPT"*. Falls back to local heuristics if no API key.
- **FastAPI** service + **Typer CLI**.
- **JSON + HTML reports** with Jinja2.
- **Education mode**: each finding includes *how it was found* and *a tutorial-style explanation.*

⚠️ **Legal/Ethical**: Scan and intercept only systems you own or have explicit written permission to test. You are responsible for your use of this software.

---

## Quickstart

```bash
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # fill in OPENAI_API_KEY if you have one
```

### Run API server
```bash
uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload
```

### CLI scan
```bash
python -m reaperscanner.cli scan https://target.tld --max-pages 200 --report reports/scan.html --json-out reports/scan.json
```

### Intercept proxy (optional)
1. Start mitmproxy with our addon:
   ```bash
   mitmproxy -s src/reaperscanner/proxy_addon.py
   ```
2. Point your browser/app at the proxy and click *"Analyze with GPT"* via the API:
   ```bash
   curl -X POST http://localhost:8000/analyze -H "Content-Type: application/json" -d @examples/flow-example.json
   ```

---

## Features (MVP)

- **Crawler**: respects robots.txt by default (can disable), extracts links/forms, queues with deduplication.
- **Checks** (examples):
  - Reflected XSS hints
  - LFI/RFI patterns (`../`, `%2e%2e/`, `php://`, `file://`)
  - File Upload misconfig heuristics (MIME/extension bypass hints, unsanitized filenames)
  - Basic SQLi signatures in params/headers
- **AI Advisor**:
  - `POST /analyze` to send any HTTP exchange or raw URL+params.
  - Returns probable vuln class, confidence, tutorial-style steps, and reproduction ideas.
- **Reports**: pretty HTML + machine-readable JSON. Education sections included.

## Config

Copy `.env.example` to `.env` and set:
- `OPENAI_API_KEY` — optional
- `OPENAI_MODEL` — default `gpt-5-thinking`
- `TIMEOUT_SECONDS` — default `20`

## Dev Tips

- Add new detectors under `src/reaperscanner/detectors/` implementing `BaseDetector`.
- Use `Finding.education` to attach *how we found it* and *what to try next*.
- Prefer async I/O in crawler & probes.

## Roadmap Ideas
- Headless browser crawler (Playwright) for JS-heavy apps
- Parametric fuzzing + wordlists
- Upload playground to exercise file-type MIME confusion
- Auth workflows and CSRF handling
- Rich React UI (shadcn) consuming the FastAPI

---

© 2025. MIT License.
