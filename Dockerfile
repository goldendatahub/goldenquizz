FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*
RUN pip install uv

WORKDIR /app
RUN git clone --depth=1 https://github.com/goldendatahub/goldenquizz.git .
RUN uv pip install --system -e .

EXPOSE 8080
CMD ["python", "-m", "goldenquizz.server"]
