from scrapy.http import Response
from news_bot.helpers.new_article_item import new_article_item
from .base_spider import BaseEntertainmentSpider


class TmzSpider(BaseEntertainmentSpider):
    name = "entertainment_tmz_spider"
    allowed_domains = ["www.tmz.com"]
    start_urls = ["https://www.tmz.com"]

    def parse(self, response: Response, **kwargs):
        articles_selector = 'article'
        link_selector = 'a::attr(href)'
        img_selector = 'img::attr(src)'
        title_selector = '.article__header-title span::text'

        articles = response.css(articles_selector)

        for article in articles:
            titles = article.css(title_selector).getall()
            img = article.css(img_selector).get()
            link = articles.css(link_selector).get()

            # format titles and join them
            title = ' '.join(x.strip() for x in titles)

            if not title:
                continue

            item = new_article_item(
                title=title,
                image=img,
                link=link,
                category=self.category,
                tags=[self.category, 'tmz'],
                source=self.allowed_domains[0]
            )

            yield item
