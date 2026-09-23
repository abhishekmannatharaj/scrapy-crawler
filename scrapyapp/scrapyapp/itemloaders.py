import re
from itemloaders.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader
from scrapyapp.items import ChocolateProduct


def extract_clean_price(value):
    if not value:
        return 0.0
    # Uses regex to find the digits and decimals after the pound sign (e.g. £1.50 or £50.00)
    match = re.search(r"£\s*([\d,]+\.?\d*)", str(value))
    if match:
        clean_num = match.group(1).replace(",", "")
        return float(clean_num)
    # Fallback to any number found
    fallback = re.search(r"([\d,]+\.?\d*)", str(value))
    if fallback:
        return float(fallback.group(1).replace(",", ""))
    return 0.0


def clean_url(value):
    if not value:
        return ""
    if not value.startswith("http"):
        return f"https://www.chocolate.co.uk{value}"
    return value


class ChocolateProductLoader(ItemLoader):
    default_item_class = ChocolateProduct
    default_output_processor = TakeFirst()

    name_in = MapCompose(str.strip)
    price_in = MapCompose(extract_clean_price)
    url_in = MapCompose(clean_url)