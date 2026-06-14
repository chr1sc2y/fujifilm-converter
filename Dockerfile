# Fujifilm Converter - Docker image
# Zero-install on host: everything (exiftool + dnglab + python CLI) is inside.
# Two commands to use: docker build + docker run

FROM python:3.12-slim

LABEL org.opencontainers.image.title="fujifilm-converter" \
      org.opencontainers.image.description="Turn any RAW into Fujifilm DNG via EXIF patch. Lightroom film sims for everyone." \
      org.opencontainers.image.source="https://github.com/zintrulcre/fujifilm-converter"

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 1. System deps: exiftool (mandatory) + tools for fetching dnglab
RUN apt-get update && apt-get install -y --no-install-recommends \
        exiftool \
        ca-certificates \
        curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Install dnglab (the best open-source RAW->DNG for Linux in container)
# We use the portable linux binary from official latest release (no version pin in filename)
RUN set -eux; \
    arch="$(uname -m)"; \
    case "$arch" in \
        x86_64)   dnglab_asset="dnglab_linux_x64" ;; \
        aarch64|arm64) dnglab_asset="dnglab_linux_aarch64" ;; \
        *) echo "Unsupported architecture: $arch"; exit 1 ;; \
    esac; \
    echo "Downloading dnglab for $arch..."; \
    curl -fsSL -o /usr/local/bin/dnglab \
        "https://github.com/dnglab/dnglab/releases/latest/download/${dnglab_asset}"; \
    chmod +x /usr/local/bin/dnglab; \
    dnglab --version || true

# 3. Install the fujifilm-converter package (provides `fuji-convert` command)
WORKDIR /app
COPY pyproject.toml ./
COPY src/ ./src/
# Also copy legacy shims for people who still do "python3 process.py"
COPY legacy/ ./legacy/
RUN pip install --no-cache-dir -e .

# 4. Default to the nice CLI entrypoint
ENTRYPOINT ["fuji-convert"]
# Users can still override: docker run ... fuji-convert --help
# Or pass files: docker run ... fuji-convert ./photos

# Usage reminder (when running without args)
CMD ["--help"]
