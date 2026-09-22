import scrapy


class SpiderappSpider(scrapy.Spider):
    name = "spiderapp"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://chocolate.co.uk"]

    def parse(self, response):
        pass
