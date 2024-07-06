from scrapy.item import Item, Field


class ArticleItem(Item):
    title = Field()
    image = Field()
    link = Field()
    category = Field()
    tags = Field()
    source = Field()
    # digest is a unique value generated for each article, to be used for duplicate detection
    digest = Field()
    createdAt = Field()
    updatedAt = Field()
