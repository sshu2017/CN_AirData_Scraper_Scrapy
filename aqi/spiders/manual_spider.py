import urlparse
from urllib.parse import urlparse, urljoin
import scrapy
from time import localtime, strftime 
from scrapy.http import Request
from aqi.items import AqiItem

class BasicSpider(scrapy.Spider):
    name = 'manual'
    allowed_domains = 'in'
    # start on the main page
    start_urls = ['http://pm25.in']

    def parse(self, response):
        #get urls and yield requests
        for url in response.xpath('//div[@class="all"]//ul[@class="unstyled"]//li'):
            url_text = url.xpath('a/@href').extract()
            full_url = urljoin('http://pm25.in', url_text[0])
            yield Request(full_url, callback = self.parse_item, dont_filter=True)
        send_email("RasPi working fine!", "Scraper report")

    def parse_item(self, response):
        """This function parse pages of each city
        @url http://pm25.in/beijing
        @returns items 1
        @scrapes cityName timestamp table
        """
        
        item=AqiItem()
        ts = response.xpath('//div[@class="live_data_time"]/p/text()').extract()
        item['timeStamp'] = str(ts)[45:-2]
        item['cityName'] = response.xpath('//div[@class="city_name"]/h2/text()').extract()
        item['table'] = response.xpath('//tbody//tr/td/text()').extract()
        
        yield item
