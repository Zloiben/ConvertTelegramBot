FROM python:3.9
WORKDIR /app
COPY . /app

ARG MODE

RUN if [ "$MODE" = "TEST" ]; then \
        pip install --no-cache-dir -r requirements/test.txt ; \
    else \
        pip install --no-cache-dir -r requirements/PROD.txt ; \
    fi
