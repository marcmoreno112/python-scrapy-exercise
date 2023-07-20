import scrapy
import re
from urllib.parse import urljoin

class RomanceBooksSpider(scrapy.Spider):
    name = 'romance_books_spider'
    allowed_domains = ['books.toscrape.com']
    start_urls = [
            "https://books.toscrape.com/catalogue/category/books/romance_8/index.html",
            "https://books.toscrape.com/catalogue/category/books/romance_8/page-2.html",
        ]

    
    def parse(self, response):
        for article in response.xpath("//article[contains(@class, 'product_pod')]"):
            has_stock = article.xpath(".//i[@class='icon-ok']").get() is not None 

            text_price = article.xpath(".//p[@class='price_color']/text()").re_first(r'\d+\.\d+')
            number_price = float(text_price) if text_price else 0

            image_relative_url = article.xpath(".//a/img/@src").get()
            image_absolute_url = urljoin(response.url, image_relative_url)

            yield {
                "title": article.xpath(".//a/@title").get(),
                "price": number_price,
                "stock": has_stock,
                "imageUrl": image_absolute_url,
            }
