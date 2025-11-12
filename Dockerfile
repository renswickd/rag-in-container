FROM python:3.11-slim

# set a deterministic working directory
WORKDIR /app

# system deps (add any OS deps the requirements need)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy project
COPY . /app

# expose streamlit port
EXPOSE 8501

# Use environment variables from .env (set via docker-compose)
ENV PYTHONUNBUFFERED=1

# run Streamlit UI
CMD ["streamlit", "run", "ui_main.py", "--server.port", "8501", "--server.address", "0.0.0.0"]