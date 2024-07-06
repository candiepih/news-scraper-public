import scrapy
from scrapy.http import Response
from news_bot.helpers.new_article_item import new_article_item
from .base_spider import BaseSportsSpider


class BbcSportsSpider(BaseSportsSpider):
    name = "sport_news_bbc_sports_spider"
    allowed_domains = ["bbc.com"]
    start_urls = ["https://www.bbc.com/sport"]

    def parse(self, response: Response, **kwargs):
        articles_selector = 'li'
        link_selector = 'a::attr(href)'
        img_selector = 'img::attr(src)'
        title_selector = 'a p span::text'

        articles = response.css(articles_selector)

        for article in articles:
            image = article.css(img_selector).get()
            link = article.css(link_selector).get()
            title = article.css(title_selector).get()

            if not image or not link or not title:
                continue

            # check total words length in title so as to avoid short titles
            if len(title.split()) <= 3:
                continue

            item = new_article_item(
                title=title.strip(),
                image=image,
                link="https://www.{}{}".format(self.allowed_domains[0], link),
                category=self.category,
                tags=[self.category, 'sports', 'bbc sports'],
                source=self.allowed_domains[0]
            )

            yield item
