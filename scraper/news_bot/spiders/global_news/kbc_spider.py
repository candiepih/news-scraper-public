import scrapy
from scrapy.http import Response
from news_bot.helpers.new_article_item import new_article_item
from .base_spider import BaseGlobalNewsSpider


class KBCSpider(BaseGlobalNewsSpider):
    name = "global_news_kbc_spider"
    allowed_domains = ["kbc.co.ke"]
    start_urls = ["https://www.kbc.co.ke/"]

    def parse(self, response: Response, **kwargs):
        articles_selector = '.td_module_wrap'
        link_selector = 'h3 a::attr(href)'
        img_selector = 'img::attr(data-img-url)'
        title_selector = 'h3 a::text'

        articles = response.css(articles_selector)

        for article in articles:
            image = article.css(img_selector).get()
            link = article.css(link_selector).get()
            title = article.css(title_selector).get()

            if not image or not link or not title:
                continue

            item = new_article_item(
                link=link,
                image=image,
                title=title.strip(),
                category=self.category,
                tags=[self.category, 'Africa', 'Kenya', 'KBC'],
                source=self.allowed_domains[0]
            )

            yield item
