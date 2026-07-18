# The default PyPI Pillow wheel (used by Render's native Python buildpack)
# does NOT include raqm/HarfBuzz text-shaping support -- confirmed directly
# by testing (Pashto letters rendered disconnected). raqm has to be present
# as a system library BEFORE Pillow is built, so Pillow's own build step can
# detect and link against it -- this is the standard, documented way to get
# a raqm-enabled Pillow on Linux when the prebuilt wheel doesn't include it.
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libraqm-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libfreetype6-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# --no-binary=Pillow forces Pillow to build from source here instead of
# using the prebuilt wheel, which is what actually lets it pick up the
# system libraqm installed above.
RUN pip install --no-cache-dir --no-binary=Pillow -r requirements.txt

COPY . .

EXPOSE 10000
# Shell form (not exec/array form) so $PORT actually gets substituted --
# Render injects PORT at runtime and expects the container to listen on it.
CMD gunicorn app:app --bind 0.0.0.0:${PORT:-10000}
