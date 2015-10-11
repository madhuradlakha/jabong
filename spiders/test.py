from scrapy.exceptions import CloseSpider
from scrapy.spider import Spider
from scrapy.http import Request
from jabong.items import JabongItem

class JabongSpider(Spider):
    name = "jabong"
    allowed_domains = ["jabong.com"]
    start_urls = ["http://www.jabong.com/women/clothing/kurtas-suit-sets/kurtas-kurtis/?page=1"]
    page_index = 1

    BASE_URL = 'http://www.jabong.com/'

    def parse(self, response):
        products = response.xpath("//li[@data-url]")
        if products:
            for product in products:
                link = product.xpath('@data-url').extract()
                link = self.BASE_URL + link[0] if link else ''
                sku = product.xpath('@data-sku').extract()
                sku = sku[0].strip() if sku else 'n/a'
                brand = product.xpath('.//span[contains(@class, "qa-brandName")]/text()').extract()
                brand = brand[0].strip() if brand else 'n/a'
                img = product.xpath('.//img[contains(@class, "itm-img")]/@src').extract()
                img = img[0].strip() if img else 'n/a'
                item = JabongItem()
                item['link'] = link
                item['sku'] = sku
                item['brand'] = brand
                item['img'] = img
                if link:
                    yield Request(url=link, callback=self.parse_page2, meta={'item': item})

        else:
            return

        self.page_index += 1
        yield Request(url="http://www.jabong.com/women/clothing/kurtas-suit-sets/kurtas-kurtis/?page=1%s" % (self.page_index + 1),
                          callback = self.parse, dont_filter = True)

    def parse_page2(self, response):
        item = response.meta['item']
        # add whatever extra details you want to item
        yield item