import scrapy
from scrapy.http import Response
from news_bot.helpers.new_article_item import new_article_item
from .base_spider import BaseGlobalNewsSpider


class TheGuardianSpider(BaseGlobalNewsSpider):
    name = "global_news_the_guardian_spider"
    allowed_domains = ["theguardian.com"]
    start_urls = ["https://www.theguardian.com/international"]

    def parse(self, response: Response, **kwargs):
        articles_selector = 'li'
        link_selector = 'a::attr(href)'
        img_selector = 'picture source::attr(srcset)'
        title_selector = 'h3 span::text'

        articles = response.css(articles_selector)

        for article in articles:
            image = article.css(img_selector).get()
            link = article.css(link_selector).get()
            title = article.css(title_selector).get()

            if not image or not link or not title:
                continue

            item = new_article_item(
                title=title.strip(),
                image=image,
                link='https://www.{}{}'.format(self.allowed_domains[0], link),
                category=self.category,
                tags=[self.category, 'The Guardian'],
                source=self.allowed_domains[0]
            )

            yield item
