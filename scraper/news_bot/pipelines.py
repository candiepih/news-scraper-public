# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from utils.db import init_db, create_indexes
from .items.article import ArticleItem


class MongoDBPipeline:
    def __init__(self):
        # Initialize the pipeline and connect to the MongoDB client
        self.db = init_db()
        self.collections = {}

    def close_spider(self, spider):
        # This will end DB connection when spider is interrupted or shutsdown
        self.db.client.close()

    def process_item(self, item: ArticleItem, spider):
        item_adapter = ItemAdapter(item)
        item_digest = item_adapter.get('digest')

        collection_name = item_adapter.get('category')
        collection = self.collections.get(collection_name)

        if collection is None:
            collection = self.db[collection_name]
            # Create indexes for the collection
            create_indexes(collection)
            # Save the collection in the cache
            self.collections[collection_name] = collection

        # insert only if the item does not exist
        collection.update_one({'digest': item_digest}, {'$set': item_adapter.asdict()}, upsert=True)

        return item
