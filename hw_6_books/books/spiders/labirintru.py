import scrapy
from scrapy.http import HtmlResponse
from books.items import BooksItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/история/?stype=0&display=table']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//div[@class="pagination-next"]/a[@class="pagination-next__text"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@class='book-qtip']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        url = response.url
        book_id = response.xpath("//div[@id='product-info']/@data-product-id").get()
        name = response.xpath("//div[@id='product-info']/@data-name").get()
        price = response.xpath("//div[@id='product-info']/@data-price").get()
        discount_price = response.xpath("//div[@id='product-info']/@data-discount-price").get()
        author = response.xpath("//div[@class='authors'][1]/a/text()").getall()
        rating = response.xpath("//div[@id='rate']/text()").get()
        yield BooksItem(url=url, _id=book_id, name=name, price=price, discount_price=discount_price,
                        author=author, rating=rating)



