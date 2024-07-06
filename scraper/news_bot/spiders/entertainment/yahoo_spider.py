from scrapy import Spider
from scrapy.http import Response
from news_bot.helpers.new_article_item import new_article_item
from .base_spider import BaseEntertainmentSpider


class YahooSpider(BaseEntertainmentSpider):
    name = "entertainment_yahoo_spider"
    allowed_domains = ["yahoo.com"]
    start_urls = ["https://yahoo.com/entertainment/"]

    def parse(self, response: Response, **kwargs):
        articles_selector = 'ul li'
        image_selector = 'img::attr(src)'
        link_selector = 'a::attr(href)'
        title_selector = 'h3 a::text'
        image_loader_url = 'https://s.yimg.com/g/images/spaceball.gif'

        articles = response.css(articles_selector)

        for article in articles:
            image = article.css(image_selector).get()
            title = article.css(title_selector).get()

            if not image or image == image_loader_url or not title:
                continue

            link = article.css(link_selector).get()
            formatted_link = self.start_urls[0].replace('/entertainment/', link)

            item = new_article_item(
                title=title.strip(),
                image=image,
                link=formatted_link,
                category=self.category,
                tags=[self.category, 'yahoo'],
                source=self.allowed_domains[0]
            )

            yield item
