FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir ".[dev]"

COPY src /app/src
COPY configs /app/configs
COPY data /app/data

ENV PYTHONPATH=/app/src
ENV APP_HOST=0.0.0.0
ENV APP_PORT=8095
ENV CONFIG_PATH=configs/policies.yaml

EXPOSE 8095
CMD ["python", "-m", "agentic_sandbox.api"]
