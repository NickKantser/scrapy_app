import os
import scrapy
from scrapy_playwright.page import PageMethod

class SrealitySpider(scrapy.Spider):
    name = 'sreality'
    root_url = 'https://www.sreality.cz/'
    items_number = 500

    def start_requests(self):
        yield scrapy.Request('https://www.sreality.cz/hledani/prodej/byty', meta=dict(
            playwright = True,
            playwright_include_page = True,
            playwright_page_methods = [
                PageMethod('wait_for_selector', 'span.norm-price.ng-binding')
            ],
            errback = self.errback,
        ))

    async def parse(self, response):
        page = response.meta['playwright_page']
        await page.close()

        for flat in response.css('div.property.ng-scope'):
            if(self.items_number <= 0):
                raise CloseSpider()
            self.items_number -= 1
            yield {
                'title': flat.css('span.name.ng-binding::text').get(),
                'image_url': flat.css('img')[2].attrib['src'],
            }

        next_page = response.css('a.paging-next').attrib['href']
        if next_page is not None:
            next_page = next_page.lstrip('/') # remove the leading '/' on the left side if it's there
            next_page = os.path.join(self.root_url, next_page)

            yield scrapy.Request(next_page, meta=dict(
                playwright = True,
                playwright_include_page = True,
                playwright_page_methods = [
                    PageMethod('wait_for_selector', 'span.norm-price.ng-binding')
                ],
                errback = self.errback,
            ))


    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()
