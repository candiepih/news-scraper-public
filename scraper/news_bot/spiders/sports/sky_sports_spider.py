import scrapy
from scrapy.http import Response
from news_bot.helpers.new_article_item import new_article_item
from news_bot.helpers.format_link import format_link
from .base_spider import BaseSportsSpider


class SkySportsSpider(BaseSportsSpider):
    name = "sport_news_sky_sports_spider"
    allowed_domains = ["skysports.com"]
    start_urls = ["https://www.skysports.com/"]

    def parse(self, response: Response, **kwargs):
        articles_selector = '.sdc-site-tile--has-link'
        link_selector = 'h3 a::attr(href)'
        img_selector = 'figure picture img::attr(src)'
        title_selector = 'h3 a span::text'

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
                link=format_link(link, self.allowed_domains[0]),
                category=self.category,
                tags=[self.category, 'sports', 'sky sports'],
                source=self.allowed_domains[0]
            )

            yield item
