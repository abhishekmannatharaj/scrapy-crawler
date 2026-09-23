import scrapy

from scrapyapp.itemloaders import ChocolateProductLoader

class SpiderappSpider(scrapy.Spider):
    name = "spiderapp"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):

        products = response.css('product-item')
        for product in products:
            loader = ChocolateProductLoader(selector=product, response=response)
            loader.add_css('name', 'a.product-item-meta__title::text')
            loader.add_css('price', 'span.price::text')
            loader.add_css('url', 'div.product-item-meta a::attr(href)')
            yield loader.load_item()

        next_page = response.css('[rel="next"] ::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)