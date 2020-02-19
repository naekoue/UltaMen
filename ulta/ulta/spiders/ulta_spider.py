from scrapy import Spider, Request
from ulta.items import UltaItem
from math import floor
import re

class BudgetSpider(Spider):
    name = "ulta_spider"
    allowed_urls = ['https://www.ulta.com/']
    start_urls = ['https://www.ulta.com/men-skin-care?N=27ck',
                    'https://www.ulta.com/men-shaving?N=u99ul3',
                    'https://www.ulta.com/men-body-care?N=wpkeo8',
                    'https://www.ulta.com/men-cologne?N=1wrfdjd',
                    'https://www.ulta.com/men-hair?N=26zv']


    def parse(self, response):

        # count total of items in the category
        items_total = response.xpath('//h2[@class="search-res-title"]/span/text()').extract_first()
        items_total = int(items_total)

        # all urls for items on the page
        #items = response.xpath('//div[@id="product-category-cont"]//ul/li')
        # items = response.xpath('//div[@class="quick-view-prod"]')


        # Number of items/page
        # items_per_page = len(items)

        # Product list pages to crawl
        #max_page = floor(items_total / items_per_page) * items_per_page
        max_page = items_total // 96 + 1
        #num_list = list(range(0,max_page+1,items_per_page))
        #base_url = re.sub("&.*","",response.request.url)
        #pages_urls = [base_url+"&No="+str(n) for n in num_list]
        pages_urls  =  [response.url + "&No={}&Nrpp=96".format(i*96) for i in range(max_page)]
     
        # for every page, get the list of urls for all products
        
        for page in pages_urls:
            #print("\n\n\n"+"Item page to crawl: ",page+'\n\n\n')
            yield Request(url = page, callback=self.parse_results_page)
            #yield scrapy.Request(url = page, callback=self.parse_results_page)       

    # Parse individual results page to get urls of product pages
    def parse_results_page(self, response):
        #product_urls = response.xpath('//div[@id="product-category-cont"]//ul/li')
        #product_urls = response.xpath('//div[@class="quick-view-prod"]')
        #prod_urls = ["https://www.ulta.com"+i.xpath('.//a/@href').extract()[0] for i in prod_urls]
        #product_urls = ["https://www.ulta.com"+i.xpath('.//a/@href').extract()[0] for i in product_urls]
        product_urls = response.xpath('//div[@class="quick-view-prod"]/a/@href').extract()
        product_urls = ["https://www.ulta.com" + url for url in product_urls]

        for prod in product_urls:
            yield Request(url=prod, callback=self.parse_prod_page)
            #yield Request(url=url, callback=self.parse_single_review_page, meta=response.meta)

    # Parse individual product page to get data on each product
    def parse_prod_page(self, response):
        # Brand
        try:
            brand = response.xpath('//div[@class="ProductMainSection__brandName"]/a/p/text()').extract_first()
        #except IndexError:
        except:
            brand = "None"

        # Product name
        try:
            product= response.xpath('//div[@class="ProductMainSection__productName"]/span/text()').extract_first()
        except:
            product = "None"

        # Ingredients
        #try:
        #   ingredients = response.xpath('//div[@class="ProductDetail__ingredients"]/div[2]//text()').extract()[0]
        #except:
            #ingredients = "None"

        # Product size and size unit
        #try:
        #   size_info = response.xpath('//p[@class="ProductMainSection__itemNumber"]/text()').extract()
        #   size = size_info[0]
        #   size_unit = size_info[2]
        # except:
        #   size_info = "None"
        #   size_unit = "None"

        # Price 
        try:
            price = response.xpath('//span[@class="Text Text--title-6 Text--left Text--bold Text--small Text--neutral-80"]/text()').extract_first()
        # 
        #response.xpath('//div[@class="ProductPricingPanel ProductPricingPanel--additionalInfo"]/span/text()').extract_first()
        except:
            price = "None"

        # Description 
        #try:
         #   description = response.xpath('//div[@class="ProductDetail__productContent"]/text()').extract_first()
        #except:
        #    description = "None"

        # Count of reviews
        try:
            #review_count = response.xpath('//span[@class="prodCellReview"]/a/text()').extract_first()
            review_count = response.xpath('//div[@class="productQvContainer"]/span[@class="prodCellReview"]/a/text()').extract_first()
        except:
            review_count = "None"

        # Review avg rating
        try:
            #review_avg_rating = response.xpath('//label[@class="sr-only"]/text()').extract_first()
            review_avg_rating = response.xpath('/a//label[@class="sr-only"]/text()').extract_first()
             #response.xpath('//label[@class="sr-only"]/text()').extract_first()
              #response.xpath('//label[@class="sr-only"]/text()').extract()
        except:
            review_avg_rating = "None"

        # Category breadcrumbs
        # try:
        #     category = response.xpath('//div[@class="Breadcrumb"]/ul/li/a/text()').extract()
        # except:
        #     category = "None"

        # put everything in an item
        item = UltaItem()
        item['product'] = product
        item['brand'] = brand     
        #item['ingredients'] = ingredients 
        #item['description'] = description
        item['review_count'] = review_count
        item['price'] = price
        item['review_avg_rating'] = review_avg_rating 
        #item['review_date'] = review_date
        #item['review_details'] = review_details
        #item['review_title'] = review_title
        #item['review_location'] = review_location 
        #item['default_size'] = default_size 
        #item['category'] = category
        item["url"] = response.url



        yield item 