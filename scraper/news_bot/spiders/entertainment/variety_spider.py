import scrapy
from scrapy.http import Response
from news_bot.helpers.new_article_item import new_article_item
from .base_spider import BaseEntertainmentSpider


class VarietySpider(BaseEntertainmentSpider):
    name = "entertainment_variety_spider"
    allowed_domains = ["variety.com"]
    start_urls = ["https://variety.com"]

    def parse(self, response: Response, **kwargs):
        articles_selector = ".most-popular-sidebar .o-tease-list .o-tease-list__item"
        link_selector = '.c-title a::attr(href)'
        title_selector = '.c-title a::text'
        image_selector = 'img::attr(src)'

        articles = response.css(articles_selector)

        for article in articles:
            title = article.css(title_selector).get()

            if not title:
                continue

            link = article.css(link_selector).get()
            image = article.css(image_selector).get()

            if not title or not link:
                continue

            item = new_article_item(
                title=title.strip(),
                link=link,
                image=image,
                category=self.category,
                tags=[self.category, 'variety'],
                source=self.allowed_domains[0]
            )

            yield item
