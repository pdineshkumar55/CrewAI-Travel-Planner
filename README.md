# Travel Planner – My First CrewAI Agent

A single-agent CrewAI app. You type in a city, and a **Travel Planner** agent suggests exactly **3 places** to visit there.

## How it works

| Piece | What it does |
|-------|--------------|
| **Agent** | `Travel Planner` with a clear role, goal and backstory, `verbose=True` |
| **Task**  | Asks for exactly 3 places in the chosen city; `expected_output` defines a numbered list format |
| **Crew**  | Combines the agent and task (sequential process) |
| **Run**   | `crew.kickoff(inputs={"city": city})` fills the `{city}` placeholders and prints the result |

The city comes from `input()` when the script starts. The API key is read from the `OPENAI_API_KEY` environment variable (loaded from a local `.env` file) and is never hard-coded.

## Project structure

```
travel-planner/
├── travel_planner.py   # all the code
├── requirements.txt    # dependencies
├── .env.example        # template for your API key
├── .gitignore          # keeps .env and venv out of git
├── Dockerfile          # container image definition
├── .dockerignore       # keeps .env and venv out of the image
├── docker-compose.yml  # optional: run with Docker Compose
└── README.md
```

## Requirements

- Python 3.10 – 3.13
- An OpenAI API key

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your API key
#    Copy .env.example to .env and paste your real key into .env
```

## Run

```bash
python travel_planner.py
```

Example:

```
Enter a city you want to visit: Madurai
... (agent's verbose reasoning) ...
==================================================
Top 3 places to visit in Madurai
==================================================
1. Meenakshi Amman Temple - ...
2. Thirumalai Nayakkar Mahal - ...
3. Gandhi Memorial Museum - ...
```

## Run with Docker

Create your `.env` first (see Setup step 3). The key is passed in at runtime and
is never copied into the image (`.env` is listed in `.dockerignore`).

```bash
# Build the image
docker build -t travel-planner .

# Run it (-it is required because the script asks you to type a city)
docker run -it --rm --env-file .env travel-planner
```

Or with Docker Compose:

```bash
docker compose build
docker compose run --rm travel-planner
```

Use `docker compose run` rather than `docker compose up`, since `up` doesn't
attach your keyboard to the prompt.

## Security

- The key lives only in `.env` or your shell environment.
- `.env` is listed in `.gitignore`, so it is never committed.
- Only `.env.example` (with a placeholder) goes into the repo.

## Clean output vs. full logs

By default the script prints only the final 3 places. To watch the agent's
verbose reasoning panels, add this to `.env`:

```
SHOW_LOGS=true
```

## Changing the model

Set `MODEL` in `.env` (default: `gpt-4o-mini`). No code changes needed.