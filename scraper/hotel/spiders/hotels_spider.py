import scrapy


class HotelSpider(scrapy.Spider):
    name = 'hotels'

    start_urls = ['https://www.tripadvisor.com/Hotels-g293961-Sri_Lanka-Hotels.html']

    def parse(self, response):
        # follow links to author pages
        for href in response.css('div#MAINWRAP div.bodycon_main div.listing-title a::attr(href)'):
            yield response.follow(href, self.parse_hotel)

        # follow pagination links
        for href in response.css('div.pagination_wrapper a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_hotel(self, response):
        def extract_with_css(query):
            return response.css(query).extract()

        yield {
            'name': extract_with_css('h1::text')[0],
            # 'price':
            'location': extract_with_css('span.popIndexValidation a::text')[0],
            'rating': extract_with_css('div#btf_wrap div.overviewContent span.overallRating::text')[0],
            'details': extract_with_css('div.overviewContent div.is-6 div.detailListItem::text'),
            'star_rating': extract_with_css('div.overviewContent div.is-6 starRating::text'),
        }