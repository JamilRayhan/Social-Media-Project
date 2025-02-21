# Stage 1: Build dependencies
FROM python:3.13 AS build

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install --no-install-recommends -y \
  libpq-dev libffi-dev libssl-dev curl \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --upgrade setuptools

COPY requirements /app/requirements
RUN pip install --prefix=/install -r /app/requirements/local.txt

# Stage 2: Final Runtime Image
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install --no-install-recommends -y \
  libpq5 libjpeg62-turbo libfreetype6 curl \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir debugpy watchdog

WORKDIR /app

COPY --from=build /install /usr/local
COPY . .

# Create user
ARG UID=1001
ARG GID=1001
RUN groupadd --system --gid $GID jamil \
  && useradd --system --uid $UID --gid $GID jamil

RUN mkdir -p /app/static /app/media && chown -R jamil:jamil /app/static /app/media

RUN mkdir -p /app/logs
RUN chmod -R 777 logs

RUN mkdir -p /app/static
RUN chmod -R 777 static

# Run migrations and collectstatic as root (to avoid permission issues)
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Switch to non-root user
USER jamil

# Healthcheck
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000').status"

# Start Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
