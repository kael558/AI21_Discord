import scrapy

import warnings
warnings.filterwarnings("ignore", message="Selector got both text and root, root is being ignored", category=UserWarning)


def is_valid_paragraph(paragraph):
    paragraph = paragraph.strip()
    paragraph = paragraph.replace(' ', ' ')
    paragraph = paragraph.replace('​', ' ')

    if ' ' not in paragraph:
        return None

    if paragraph[-1].isalnum():
        return None

    if paragraph[-1] == '”':
        return None

    if paragraph[0] == '"' and paragraph[-1] == '"':
        paragraph = paragraph[1:-1]

    return paragraph


class AI21Spider(scrapy.Spider):
    name = "ai21_spider"
    allowed_domains = ['docs.ai21.com', 'ai21.com']
    start_urls = ['https://docs.ai21.com/docs/overview', 'https://www.ai21.com/']

    def parse(self, response):
        for paragraph in response.css('p').xpath('normalize-space()').getall():
            paragraph = is_valid_paragraph(paragraph)
            if paragraph:
                yield {'paragraph': paragraph, 'link': response.request.url}

        base_url = response.request.url.split('.com')[0] + '.com'
        for link in response.xpath('.//@href').getall():
            if not link.startswith("https"):
                link = base_url + link
            yield response.follow(link, self.parse)