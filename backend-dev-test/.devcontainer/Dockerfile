FROM debian:bullseye

# Update the package list and install essential packages
RUN apt-get update && apt-get install -y \
    # Core utilities
    build-essential \
    curl \
    wget \
    zip \
    unzip \
    tar \
    gzip \
    nano \
    vim \
    sudo \
    ca-certificates \
    openssl \
    software-properties-common \
    dnsutils \
    net-tools \
    python3 \
    python3-pip \
    python3-venv \
    git \
    netcat \
    apt-transport-https \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"