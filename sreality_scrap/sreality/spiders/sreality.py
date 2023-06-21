import os
import scrapy
from scrapy_playwright.page import PageMethod

class SrealitySpider(scrapy.Spider):
    name = 'sreality'
    root_url = 'https://www.sreality.cz/'
    # custom_settings = {
    #     'CLOSESPIDER_ITEMCOUNT': 50,
    #     # 'CLOSESPIDER_TIMEOUT': 2,
    # }
    items_number = 10

    def start_requests(self):
        yield scrapy.Request('https://www.sreality.cz/hledani/prodej/byty', meta=dict(
            playwright = True,
            playwright_include_page = True,
            playwright_page_methods = [
                PageMethod('wait_for_selector', 'span.norm-price.ng-binding')
            ],
            errback = self.errback,
        ))

        # yield scrapy.Request("https://www.sreality.cz/hledani/prodej/byty", meta={'playwright': True})
        # yield scrapy.Request("http://quotes.toscrape.com/js/", meta={"playwright": True})

    async def parse(self, response):
        page = response.meta['playwright_page']
        await page.close()

        for flat in response.css('div.property.ng-scope'):
        # for price in response.css('span.norm-price.ng-binding'):
            # try:
            #     price = flat.css('span.norm-price.ng-binding::text').get()
            #     price = price.
            if(self.items_number <= 0):
                raise CloseSpider()
            self.items_number -= 1
            yield {
                'title': flat.css('span.name.ng-binding::text').get(),
                'image_url': flat.css('img')[2].attrib['src'],
                # 'price_in_crowns': flat.css('span.norm-price.ng-binding::text').get(),

            }

        # if(self.items_number > 0):
        next_page = response.css('a.paging-next').attrib['href']
        if next_page is not None:
            next_page = next_page.lstrip('/') # remove the leading '/' on the left side if it's there
            next_page = os.path.join(self.root_url, next_page)
            print(f'My print: {next_page} <------------------------------------------------------------------')

            yield scrapy.Request(next_page, meta=dict(
                playwright = True,
                playwright_include_page = True,
                # callback=self.parse,
                playwright_page_methods = [
                    PageMethod('wait_for_selector', 'span.norm-price.ng-binding')
                ],
                errback = self.errback,
            ))

        # next_page = response.css('paging-next').attrib['href']
        # if next_page is not None:
        #     next_page = next_page.lstrip('/') # remove the leading '/' on the left side if it's there
        #     next_page = os.path.join(root_url, next_page)
        #
        #     # yield self.start_requests()
        #     yield scrapy.Request('https://www.sreality.cz/hledani/prodej/byty?strana=2', meta=dict(
        #         playwright = True,
        #         playwright_include_page = True,
        #         playwright_page_methods = [
        #             PageMethod('wait_for_selector', 'span.norm-price.ng-binding')
        #         ],
        #         # errback = self.errback()
        #     ))

    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()
