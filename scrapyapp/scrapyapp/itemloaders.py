from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst

from scrapyapp.items import ChocolateProduct


class ChocolateProductLoader(ItemLoader):
    default_item_class = ChocolateProduct
    default_output_processor = TakeFirst()
    name_in = MapCompose(str.strip)
    price_in = MapCompose(
        lambda x: x.split("£")[-1].strip() if "£" in x else x,
        float,
    )
    url_in = MapCompose(
        lambda x: f"https://www.chocolate.co.uk{x}"
        if not x.startswith("http")
        else x
    )