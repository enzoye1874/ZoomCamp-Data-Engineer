# base Docker image that we will build on
FROM python:3.13.11-slim

# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# set up the working directory inside the container
WORKDIR /code

# put the virtual environment created by uv on PATH
ENV PATH="/code/.venv/bin:$PATH"

# copy dependency files first so this layer is cached unless dependencies change
COPY pyproject.toml .python-version uv.lock ./

# install dependencies only (the project itself is a plain script)
RUN uv sync --locked --no-install-project --no-dev

# copy the ingestion script
COPY ingest_data.py .

# run the script; CLI options can be appended at `docker run` time
ENTRYPOINT ["python", "ingest_data.py"]
