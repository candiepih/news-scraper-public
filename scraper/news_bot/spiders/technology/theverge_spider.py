import scrapy
from scrapy.http import Response
from news_bot.helpers.new_article_item import new_article_item
from .base_spider import BaseTechnologySpider


class TheVergeSpider(BaseTechnologySpider):
    name = "tech_news_the_verge_spider"
    allowed_domains = ["theverge.com"]
    start_urls = ["https://www.theverge.com/tech"]

    def parse(self, response: Response, **kwargs):
        articles_selector = '.duet--content-cards--content-card'
        link_selector = 'h2 a::attr(href)'
        img_selector = 'a span img::attr(srcset)'
        title_selector = 'h2 a::text'

        articles = response.css(articles_selector)

        for article in articles:
            images = article.css(img_selector).get()
            link = article.css(link_selector).get()
            title = article.css(title_selector).get()

            if not images or not link or not title:
                continue

            images_set = images.split(',')

            if len(images_set) < 8:
                continue

            # get the image url
            image_set = images_set[7].strip()
            image = image_set.split()[0]

            # check total words length in title so as to avoid short titles
            if len(title.split()) <= 2:
                continue

            item = new_article_item(
                title=title.strip(),
                image=image,
                link='https://www.{}{}'.format(self.allowed_domains[0], link),
                category=self.category,
                tags=[self.category, 'the verge', 'tech news'],
                source=self.allowed_domains[0]
            )

            yield item
