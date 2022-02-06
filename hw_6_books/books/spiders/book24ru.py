import scrapy
from scrapy.http import HtmlResponse
from books.items import BooksItem


class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    page = 1
    start_urls = [f'https://book24.ru/search/?q=история']

    def parse(self, response: HtmlResponse):
        if response.status != 404:
            print(self.page)
            self.page += 1
            next_page = f'https://book24.ru/search/page-{self.page}/?q=история'
            yield response.follow(next_page, callback=self.parse)

        part_links = response.xpath('//div[@class="product-list__item"]//a[@class="product-card__name smartLink"]/@href').getall()

        for part in part_links:
            link = 'https://book24.ru' + part
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        title = response.xpath('//h1/text()').get()  # имя и автор
        url = response.url
        price = response.xpath('//span[@class="app-price product-sidebar-price__price-old"]/text()').get()
        if price:
            discount_price = response.xpath('//span[@class="app-price product-sidebar-price__price"]/text()').get()
        else:
            price = response.xpath('//span[@class="app-price product-sidebar-price__price"]/text()').get()
            discount_price = None
        rating = response.xpath("//span[@class='rating-widget__main-text']/text()").get()
        yield BooksItem(title=title, url=url, price=price, discount_price=discount_price, rating=rating)
