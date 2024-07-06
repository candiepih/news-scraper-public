# NEWS SCRAPPER

The News Scrapper project automates the extraction of news articles from a variety of sources and then serves them through an API.

It is designed to crawl websites at a specified time interval, organize the data, check for duplications and then persists the results in a database. The data can then be served via an API based on the news category.

LIVE API url: [news-api.alexnjagi.com](https://news-api.alexnjagi.com)

LIVE News Website: Coming Soon

## Folders

- [.github](./.github) - contains github actions to build docker containers and automate deployment to the servers using [kamal deploy tool](https://kamal-deploy.org/)
- [.kamal](./.kamal) - contains hooks related to [kamal](https://kamal-deploy.org/)
- [config](./config/) - contains kamal configuration files. This files are used to instuct how kamal deploys the [news_api](./news_api/) and the [scraper](./scraper/).
- [news_api](./news_api/) - Django based API for serving news results based on categories. API routes can be found by visiting [news-api.alexnjagi.com](https://news-api.alexnjagi.com)
- [scraper](./scraper/) - Contains [scrapy](https://scrapy.org/) spiders that will crawl different sites and [scrapyd](https://scrapyd.readthedocs.io/en/latest/index.html) which makes the spiders interactible using an API. Also contains cron job setup for periodic scraping

## Local Setup

1. Clone this repository by copying ssh or https link
2. This project consists of 2 folders, the [news_api](./news_api/) which handles anything concerning API and [scraper](./scraper/) containing anything to do with scraping
3. Open each project separately on your IDE of choice
4. Create a `.env` file In each folder based on the provided `.env.example` file. `NB:` This project requires Mongo DB URI and Redis instance ready.
5. If you would like to make some changes or run locally without docker, follow below steps.
    - Create a `python virtual environment` and run `pip install -r requirements.txt` in each folder. This will install all packages needed for the project.
    - Before running the [news_api](./news_api/), make sure the `.env` file is ready. Run `python manage.py runserver`. This should start on port 8000. The link on browser will be `http://localhost:8000`. The documentaion of the API will be your first view. Ignore migration warning on the console. Currently we don't need to run any migrations because we are only pulling data from Mongo DB. Also based on djongo package and django versions, it might throw an error.
    - Before running the [scraper](./scraper/) project, setup a `python virtual environment` and `.env` file like the previous step. After installing, run `scrapyd`. This should start scrapyd on port `6800`. To make sure it's working, copy `http://localhost:6800` on your browser. This should have some information about the project. To run spiders, you will need to send a POST request to scrapyd to tell it to schedule the spiders. make a post request to this path `POST http://localhost:6800/schedule.json` with the following data

    ```json
    {
        "project": "news_bot",
        "spider": "global_news_kbc_spider"
    }
    ```

    If you don't know the name of the spider to scrap, send a GET request to `GET http://localhost:6800/listspiders.json?project=news_bot` which should give you a list of available spiders in a project.

6. Running this project on docker is the same as local setup, only that the previous steps are automated.
   - Make sure docker and docker compose is installed. Here you don't need Redis on your machine, but you will need Mongo URL. The redis url should look like this `redis://redis:6379` since it points to redis instance in docker container. The docker images referenced in docker compose have already been built and can be found [here](https://hub.docker.com/repositories/candiepih) in dockerhub.
  
   - In the [scraper](./scraper/) folder before running docker compose, modify this file [Crontab](./scraper/cron/Crontab) to `0/5 0 * * * /app/cron.sh` which will allow it to scrap every 5 minutes. This is necessary because the scraper by default runs every midnight. You can now run docker compose file `docker compose -f ./deployment/docker-compose.yml up -d` which will start scrapyd scraper container and cron job container responsible for scheduling scraping jobs. To make sure it's working, visit `http://localhost:6800` in your browser.
   - In the [news_api](./news_api/) run `docker compose -f ./deployment/docker-compose.yml up -d`. This will try to reference `.env` file, so make sure it's ready. This will spin redis container and new_api container. Make sure they are ready with `docker ps`. You can then check on the browser with `http://localhost:8000`. This should show the API documentation page. The results of the API should be available in various categories in 5 minutes if you had set the crontab interval to 5 minutes

## Deploying

This project makes use of GitHub actions to build and deploy. [Kamal](https://kamal-deploy.org/) handles the deployment part based on the configuration files found [here](./config/).

You will find [news api config file](./config/deploy.news-api.yml) which details how news api is deployed. The news_api is the only service exposed to the internet on the specified domain.

You will also find [scraper config file](./config/deploy.scraper.yml) which is contains deployment instructions for the scraper and scraper cron job container. These services are not exposed to the internet.

Here are some things you will need to prepare in your server before deploying

- Installing docker manually in your server. Kamal installs docker in your server, but sometimes this might not work, especially when using AWS ec2 with Amazon based images.
- Creating folder `/var/lib/redis` manually
- Create docker network `news-scraper`. This is required so that the cron job container knows how to resolve the redis service by it's name, like `redis://news-api-redis:6379`.
