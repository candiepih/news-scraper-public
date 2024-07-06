FROM python:3.12.4-alpine AS base

# 1. Install dependencies only when needed
FROM base AS deps

RUN apk add --update --virtual .build-deps \
    build-base \
    postgresql-dev \
    python3-dev \
    libpq

RUN pip3 install --upgrade pip

# 2. Rebuild the source code only when needed
FROM deps AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt


# 3. Production image, copy all the files
FROM base AS final
RUN apk add --update curl curl-dev 

WORKDIR /app

ENV APP_USER=django

RUN addgroup -g 1001 -S python
RUN adduser -S $APP_USER -u 1001

# Copy the Django project code to the working directory
COPY --chown=django:python ./ .
COPY --from=builder --chown=django:python /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/

USER $APP_USER

RUN python manage.py collectstatic --clear --noinput

EXPOSE 8000

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
