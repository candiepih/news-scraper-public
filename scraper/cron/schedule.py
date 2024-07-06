import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = "news_bot"
# name of the service in docker-compose.yml is scraper, the
# ip of the service will be resolved by the container
HOST = os.getenv('SCRAPYD_HOST_URL')

# configure logging
FORMAT = '%(asctime)s -> %(message)s'
date_format = '%d-%b-%y %H:%M:%S'
logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt=date_format)

# f-strings require python version >= 3.6
LIST_SPIDER_URL = f"{HOST}/listspiders.json?project={PROJECT_NAME}"
SCHEDULE_SPIDER_URL = f"{HOST}/schedule.json"


def get_spiders() -> list[str]:
    """
    Makes call to scrapyd to get the list all spiders available
    Returns:
        list[str]: list of all spiders available
    """
    response = requests.get(LIST_SPIDER_URL)

    if response.status_code == 200:
        json = response.json()
        return json['spiders']
    return []


def schedule_spider(spider_name: str) -> bool:
    """
    Schedules a spider to run
    Args:
        spider_name (str): name of the spider to run
    Returns:
        bool: True if successful, False otherwise
    """
    data = {
        "project": PROJECT_NAME,
        "spider": spider_name,
    }

    response = requests.post(SCHEDULE_SPIDER_URL, data=data)

    if response.status_code == 200:
        return True
    raise Exception(f"Failed to schedule ${spider_name} spider")


def crawl():
    """
    Schedules all spiders to run
    Returns:
        None
    """
    spiders = get_spiders()

    for spider in spiders:
        schedule_spider(spider)
        logging.info(f"scheduled spider ({spider})")


if __name__ == '__main__':
    # make the call to scrapyd to schedule all spiders
    crawl()
