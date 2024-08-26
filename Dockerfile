###########
# BUILDER #
###########

# Pull python to build dependencies
FROM python:3.11-slim as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
COPY ./local-requirements.txt .
RUN pip3 wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r local-requirements.txt

FROM bitnami/java:22.0.2-11

WORKDIR /home/courserekt

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install python
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3 python3-pip

COPY . .

# install dependencies from builder
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/local-requirements.txt .
RUN pip install --upgrade pip --break-system-packages
RUN pip install --no-cache /wheels/* --break-system-packages

# run scraper
RUN python3 -m src.history.build

# run web
CMD python3 -m src.web.main
