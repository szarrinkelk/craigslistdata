from craigslist.items import CraigslistItem
import scrapy
from scrapy.selector import HtmlXPathSelector

class CraigsSpider(scrapy.Spider):
	name = "craigsBase"
	allowed_domains = ["craigslist.org"]
	start_urls = ["http://sfbay.craigslist.org/search/npo"]

	def parse(self, response):
		#crawls all the links
		for href in response.css("span.pl > a::attr('href')"):
			url = response.urljoin(href.extract())
			print(url)
			yield scrapy.Request(url, callback=self.parse_dir_contents)


	def parse_dir_contents(self, response):
		item = CraigslistItem()
		item['title'] = response.xpath('//*[@id="titletextonly"]/text()').extract()
		item['comp'] = response.xpath('//*[@id="pagecontainer"]/section/section/div[1]/p/span[1]/b/text()').extract()
		yield item


#scrapy crawl craigsBase -o craigfile.csv -t csv

