import hashlib
from itemadapter import ItemAdapter
from datetime import datetime
from news_bot.items.article import ArticleItem


def new_article_item(**data) -> ArticleItem:
    adapter = ItemAdapter(data)

    article_item = ArticleItem()

    link = adapter.get('link')
    digest = hashlib.md5(link.encode()).hexdigest()

    article_item['title'] = adapter.get('title')
    article_item['image'] = adapter.get('image')
    article_item['link'] = adapter.get('link')
    article_item['category'] = adapter.get('category')
    article_item['tags'] = adapter.get('tags')
    article_item['source'] = adapter.get('source')

    article_item['digest'] = digest
    article_item['createdAt'] = datetime.now()
    article_item['updatedAt'] = datetime.now()

    return article_item
