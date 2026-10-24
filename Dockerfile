FROM python:3.12-slim

# No .pyc files, and print output immediately (no buffering).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install dependencies first so this layer is cached between code changes.
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY travel_planner.py .

# Run as a non-root user. CrewAI writes some local data under $HOME.
RUN useradd --create-home appuser
USER appuser

# The API key is passed in at runtime (--env-file .env), never baked in.
CMD ["python", "travel_planner.py"]
