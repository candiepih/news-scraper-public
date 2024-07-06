import scrapy
from scrapy.http import Response
from news_bot.helpers.new_article_item import new_article_item
from .base_spider import BaseTechnologySpider


class GizmodoSpider(BaseTechnologySpider):
    name = "tech_news_gizmodo_spider"
    allowed_domains = ["gizmodo.com"]
    start_urls = ["https://gizmodo.com/science"]

    def parse(self, response: Response, **kwargs):
        articles_selector = 'article'
        link_selector = 'a::attr(href)'
        img_selector = 'picture source::attr(data-srcset)'
        title_selector = 'a h4::text'

        articles = response.css(articles_selector)

        for article in articles:
            image = article.css(img_selector).get()
            link = article.css(link_selector).get()
            title = article.css(title_selector).get()

            if not image or not link or not title:
                continue

            # check total words length in title so as to avoid short titles
            if len(title.split()) <= 2:
                continue

            item = new_article_item(
                title=title.strip(),
                image=image,
                link=link,
                category=self.category,
                tags=[self.category, 'gizmodo'],
                source=self.allowed_domains[0]
            )

            yield item
