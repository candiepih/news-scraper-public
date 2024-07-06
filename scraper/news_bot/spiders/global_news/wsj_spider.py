import scrapy
from scrapy.http import Response
from news_bot.helpers.new_article_item import new_article_item
from .base_spider import BaseGlobalNewsSpider


class WSJSpider(BaseGlobalNewsSpider):
    name = "global_wall_street_journal_spider"
    allowed_domains = ["wsj.com"]
    start_urls = ["https://www.wsj.com"]

    def parse(self, response: Response, **kwargs):
        articles_selector = 'article'
        link_selector = 'a::attr(href)'
        img_selector = 'img::attr(src)'
        title_selector = 'img::attr(alt)'

        articles = response.css(articles_selector)

        for article in articles:
            image = article.css(img_selector).get()
            link = article.css(link_selector).get()
            title = article.css(title_selector).get()

            if not image or not link or not title:
                continue

            item = new_article_item(
                title=title,
                image=image,
                link=link,
                category=self.category,
                tags=[self.category, 'wsj'],
                source=self.allowed_domains[0]
            )

            yield item
