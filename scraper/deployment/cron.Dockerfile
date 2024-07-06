FROM python:3.12.4-alpine AS base

# 1. Install dependencies only when needed
FROM base AS base_deps

RUN apk add --update --update --virtual .build-deps \
    build-base \
    python3-dev \
    libpq

RUN pip3 install --upgrade pip

# 2. Rebuild the source code only when needed
FROM base_deps AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --no-cache-dir requests
RUN pip3 install --no-cache-dir python-dotenv

# 3. Production image, copy all the files
FROM base AS final
RUN apk add --update curl curl-dev apk-cron

WORKDIR /app

ENV APP_USER=scrapy_cron
ENV APP_GROUP=python

RUN addgroup -g 1001 -S $APP_GROUP
RUN adduser -S $APP_USER -u 1001

# Create the log file to be able to run tail
# RUN mkdir -p /app/log/scrapy/
# Create cron directory
RUN mkdir -p /etc/cron.d

RUN chmod 755 /etc/cron.d
RUN chown -R $APP_USER:$APP_GROUP /etc/cron.d
RUN chown -R $APP_USER:$APP_GROUP /app
# RUN chown -R $APP_USER:$APP_GROUP /app/log/scrapy/

# copy cron related files
COPY --chown=$APP_USER:$APP_GROUP ./cron .
COPY --from=builder --chown=$APP_USER:$APP_GROUP /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/

# Ensure the cron.sh is executable
RUN chmod u+x cron.sh
# Move Crontab file to the cron.d directory

RUN crontab -u $APP_USER Crontab

# RUN touch /app/log/scrapy/cron.log

# Run cron, and tail the primary cron log
#CMD crond && tail -f /app/log/scrapy/cron.log
#CMD ["/usr/sbin/crond", "-f", "-d", "8"]
CMD ["crond", "-f", "-l", "2"]
