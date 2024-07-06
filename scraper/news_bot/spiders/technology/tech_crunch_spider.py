import scrapy
from scrapy.http import Response
from news_bot.helpers.new_article_item import new_article_item
from .base_spider import BaseTechnologySpider


class TechCrunchSpider(BaseTechnologySpider):
    name = "tech_news_techcrunch_spider"
    allowed_domains = ["techcrunch.com"]
    start_urls = ["https://techcrunch.com/"]

    def parse(self, response: Response, **kwargs):
        articles_selector = '.wp-block-tc23-post-picker'
        link_selector = 'a::attr(href)'
        img_selector = 'img::attr(src)'
        title_selector = 'a::text'

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
                tags=[self.category, 'techcrunch'],
                source=self.allowed_domains[0]
            )

            yield item
