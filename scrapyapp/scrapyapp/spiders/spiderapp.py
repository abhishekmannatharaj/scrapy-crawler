import scrapy

from scrapyapp.itemloaders import ChocolateProductLoader

class SpiderappSpider(scrapy.Spider):
    name = "spiderapp"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):
        products = response.xpath("//product-item")
        for product in products:
            loader = ChocolateProductLoader(selector=product, response=response)
            loader.add_xpath("name", ".//a[contains(@class, 'product-item-meta__title')]//text()")
            loader.add_xpath("price", ".//*[contains(concat(' ', normalize-space(@class), ' '), ' price ')]")
            product_url = product.xpath(
                ".//div[contains(@class, 'product-item-meta')]//a/@href"
            ).get()
            loader.add_value("url", response.urljoin(product_url) if product_url else "")
            yield loader.load_item()

        next_page = response.xpath("//*[@rel='next']/@href").get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)