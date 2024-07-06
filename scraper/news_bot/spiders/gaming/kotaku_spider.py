import scrapy
from scrapy.http import Response
from news_bot.helpers.new_article_item import new_article_item
from .base_spider import BaseGamingSpider


class KotakuSpider(BaseGamingSpider):
    name = "gaming_news_kotaku_spider"
    allowed_domains = ["kotaku.com"]
    start_urls = ["https://kotaku.com/"]

    def parse(self, response: Response, **kwargs):
        articles_selector = 'article'
        link_selector = 'a::attr(href)'
        img_selector = 'picture source::attr(srcset)'
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
                tags=[self.category, 'gaming', 'Kotaku'],
                source=self.allowed_domains[0]
            )

            yield item
