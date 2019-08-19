# -*- coding: utf-8 -*-
import scrapy


class PetloveSpider(scrapy.Spider):
    name = 'petlove'
    base_url = 'https://www.petlove.com.br/cachorro'

    def generate_urls(self, n_pages=100):
        for p in range(1, n_pages):
            yield '{}?page={}'.format(self.base_url, p)

    def start_requests(self):
        urls = self.generate_urls()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        selector = 'a.product-wrapper::attr(href)'
        for product_url in response.css('div#shelf-loop a::attr(href)'):
            yield response.follow(product_url, self.parse_product)

    def parse_product(self, response):
        name = response.css('h1::text').extract_first()
        description = name.join(response.css('div.tab-details::text').extract())
        categories = response.xpath(
            '//*[@id="product"]/div/div/div[1]/div[1]/ul/li[*]/a/span/text()'
        )
        category = ','.join(categories[:-1].extract())

        yield dict(name=name, description=description, category=category)
