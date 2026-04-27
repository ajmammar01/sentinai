# SentinAI

SentinAI is a stateless FastAPI email analyzer that classifies incoming email content and returns structured AI output in real time.

This project is intentionally built for privacy: requests are processed in memory and no ticket/database persistence is used.

## Features

- Stateless architecture (no database writes, no stored user messages)
- FastAPI backend with a clean JSON analysis endpoint
- Jinja2-powered single-page portal for input + result display
- Structured AI output (`ticket` or `flagged`) via OpenAI
- Lightweight local setup for development

## Project Structure

```text
sentinai/
├─ app/
│  ├─ api/
│  │  └─ routes.py              # GET / and POST /analyze-only
│  ├─ services/
│  │  └─ processor.py           # Email analysis orchestration
│  ├─ infrastructure/
│  │  └─ llm_client.py          # OpenAI client + .env loading
│  ├─ domain/
│  │  ├─ entities.py            # Pydantic response schemas
│  │  └─ enums.py               # Classification enums
│  └─ .env                      # Environment variables (local only)
├─ templates/
│  └─ index.html                # Frontend portal UI
├─ main.py                      # FastAPI app entrypoint
├─ requirements.txt             # Python dependencies
└─ .gitignore
```

## Setup

### 1) Clone and enter the project

```bash
git clone <your-repo-url>
cd sentinai
```

### 2) Create and activate a virtual environment

On Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Create environment file in `app/`

Create `app/.env` with:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## Run the App (via `main.py`)

```bash
python main.py
```

The app runs on:

- `http://127.0.0.1:8000/` — web portal
- `http://127.0.0.1:8000/analyze-only` — JSON analysis endpoint (POST)

## API Usage

### POST `/analyze-only`

Request body:

```json
{
  "content": "From: user@example.com\nSubject: Billing issue\n..."
}
```

Returns structured JSON for either:

- `type: "ticket"` with category/urgency/summary/action items, or
- `type: "flagged"` with reason.

## Privacy Model

SentinAI is designed as a utility-style analyzer:

- No database layer
- No message persistence
- Results are shown in the UI and cleared on refresh

