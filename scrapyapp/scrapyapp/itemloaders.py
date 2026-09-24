import re
from itemloaders.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader
from scrapyapp.items import ChocolateProduct
from w3lib.html import remove_tags


def extract_clean_price(value):
    if not value:
        return None

    text = remove_tags(str(value))
    text = " ".join(text.split())
    match = re.search(r"(?:£|GBP)\s*([\d,]+(?:\.\d{1,2})?)", text, re.IGNORECASE)
    if match:
        clean_num = match.group(1).replace(",", "")
        return float(clean_num)

    fallback = re.search(r"([\d,]+(?:\.\d{1,2})?)", text)
    if fallback:
        return float(fallback.group(1).replace(",", ""))
    return None


def clean_url(value):
    if not value:
        return ""
    return value.strip()


class ChocolateProductLoader(ItemLoader):
    default_item_class = ChocolateProduct
    default_output_processor = TakeFirst()

    name_in = MapCompose(str.strip)
    price_in = MapCompose(extract_clean_price)
    url_in = MapCompose(clean_url)