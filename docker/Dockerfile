# syntax=docker.io/docker/dockerfile:1

# Development Dockerfile

# Stage 1: Build Stage
FROM python:3.13 AS build

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install required system dependencies for building Python packages
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Upgrade setuptools for better package management
RUN pip install --upgrade setuptools

# Copy the requirements file and install dependencies early to leverage caching
COPY requirements /app/requirements
RUN pip install --prefix=/install -r /app/requirements/local.txt

# Stage 2: Final Stage
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install runtime dependencies and development tools
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq5 \
    libjpeg62-turbo \
    libfreetype6 \
    vim \
    git \
    net-tools \
  && rm -rf /var/lib/apt/lists/*

# Install additional tools for debugging and hot reloading
RUN pip install --no-cache-dir debugpy watchdog

# Set the working directory inside the container
WORKDIR /app

# Copy installed Python packages from the build stage
COPY --from=build /install /usr/local

# Copy the rest of the application code
COPY . .

# Ensure entrypoint script has execution permissions
COPY docker/entrypoint.sh /app/docker/entrypoint.sh
RUN chmod +x /app/docker/entrypoint.dev.sh

# Set default UID/GID (can be overridden)
ARG UID=1001
ARG GID=1001

# Create group and user dynamically
RUN addgroup --system --gid $GID jamil \
  && adduser --system --uid $UID --ingroup jamil jamil \
  && mkdir -p /app/static /app/media \
  && chown -R jamil:jamil /app

# Set the user for the container
USER jamil

# Set the entry point to the development script
ENTRYPOINT ["/app/docker/entrypoint.sh"]
