# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import json
from importlib import import_module

from itemadapter import ItemAdapter


class ScrapyappPipeline:
    def process_item(self, item, spider):
        return item


class PostgresPipeline:
    def __init__(self, dsn):
        self.dsn = dsn

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings["POSTGRES_DSN"])

    def open_spider(self, spider):
        psycopg = import_module("psycopg")
        self.connection = psycopg.connect(self.dsn)
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS products ("
            "name TEXT, price NUMERIC, url TEXT PRIMARY KEY)"
        )
        self.connection.commit()

    def process_item(self, item, spider):
        data = ItemAdapter(item)
        self.connection.execute(
            "INSERT INTO products (name, price, url) VALUES (%s, %s, %s) "
            "ON CONFLICT (url) DO UPDATE SET name = EXCLUDED.name, price = EXCLUDED.price",
            (data.get("name"), data.get("price"), data.get("url")),
        )
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.connection.close()


class MongoPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler.settings["MONGODB_URI"],
            crawler.settings["MONGODB_DATABASE"],
            crawler.settings["MONGODB_COLLECTION"],
        )

    def __init__(self, uri, database, collection):
        self.uri = uri
        self.database = database
        self.collection = collection

    def open_spider(self, spider):
        pymongo = import_module("pymongo")
        self.client = pymongo.MongoClient(self.uri)
        self.products = self.client[self.database][self.collection]

    def process_item(self, item, spider):
        data = dict(ItemAdapter(item))
        self.products.replace_one({"url": data["url"]}, data, upsert=True)
        return item

    def close_spider(self, spider):
        self.client.close()


class RedisPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings["REDIS_URL"])

    def __init__(self, url):
        self.url = url

    def open_spider(self, spider):
        redis = import_module("redis")
        self.client = redis.from_url(self.url)

    def process_item(self, item, spider):
        self.client.rpush("scrapyapp:products", json.dumps(dict(ItemAdapter(item))))
        return item


class RabbitMQPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings["RABBITMQ_URL"], crawler.settings["RABBITMQ_QUEUE"])

    def __init__(self, url, queue):
        self.url = url
        self.queue = queue

    def open_spider(self, spider):
        pika = import_module("pika")
        self.connection = pika.BlockingConnection(pika.URLParameters(self.url))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)

    def process_item(self, item, spider):
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            body=json.dumps(dict(ItemAdapter(item))).encode("utf-8"),
            properties=self._delivery_mode(),
        )
        return item

    def _delivery_mode(self):
        pika = import_module("pika")
        return pika.BasicProperties(delivery_mode=2)

    def close_spider(self, spider):
        self.connection.close()
