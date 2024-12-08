FROM mcr.microsoft.com/devcontainers/base:noble
RUN apt-get update && apt-get install -y \
    git \
    python3.12 \
    python3-pip \
    python3-venv
COPY requirements.txt .
RUN python3 -m venv .venv && . .venv/bin/activate && python3 -m pip install -r requirements.txt && python3 -m pip install -r requirements.txt