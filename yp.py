import scrapy

class YPSpider(scrapy.Spider):
    name = 'yp'
    # start_urls = ['http://www.yp.com.hk/Transportation-Logistics-b/Moving-Warehousing-Courier-Logistics-Services/Logistics-Management-Services/p1/ch/']

    # Random first page
    start_urls = [
        'http://www.yp.com.hk/Business-Professional-Services-b/ch/',
    ]

    custom_settings = {
        'FEED_EXPORT_ENCODING': 'big5',
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'file.csv',
        'LOG_LEVEL': 'ERROR',
        'LOG_STDOUT': True
    }

    def parse(self, response):
        print("hihi")
        for category in response.css('#ContentPlaceHolder_Body_Label_Left > ul > li'):
            url = response.urljoin(category.css('a::attr(href)').extract_first())
            yield scrapy.Request(url=url, callback=self.parse_cat)

    def parse_cat(self, response):
        for category in response.css('#ContentPlaceHolder_Body_Label_Right > ul > li'):
            url = response.urljoin(category.css('a::attr(href)').extract_first())
            yield scrapy.Request(url=url, callback=self.parse_sub_cat)

    def parse_sub_cat(self, response):
        for category in response.css('#ContentPlaceHolder_Body_Label_Right > ul > li'):
            url = response.urljoin(category.css('a::attr(href)').extract_first())
            yield scrapy.Request(url=url, callback=self.parse_company)

    # Scrape company pages
    def parse_company(self, response):
        for company in response.css('.listing_div'):
            yield {
                'Company Name': company.css('.cname::text, .cname > a::text').extract_first(),
                'Tags': company.css('.category > li > a::text').extract(),
                'Phone': company.css('.tbl_addr td:nth-child(1) a::text, .tbl_addr td:nth-child(1) nobr::text').extract_first(),
                'Address': company.css('.tbl_addr td:nth-child(2) span::text').extract_first()
            }

        for next_page in response.css('.srh_pgnum a.bluelink.overunder'):
            yield response.follow(next_page, self.parse)