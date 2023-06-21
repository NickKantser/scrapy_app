import scrapy
import json

class SrealitySpider(scrapy.Spider):
    name = 'sreality'
    start_urls = ['https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page=20']
    page_number = 2
    item_count = 0
    max_items_number = 500

    def parse(self, response):
        json_response = json.loads(response.text)
        estates = json_response['_embedded']['estates']

        for estate in estates:
            if self.item_count == self.max_items_number:
                raise CloseSpider()

            self.item_count += 1
            yield {
                'title': estate['name'],
                'image_url' : estate['_links']['images'][0]['href']
            }

        next_page = f'https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page=20&page={self.page_number}'
        self.page_number += 1

        yield response.follow(next_page, callback=self.parse)
