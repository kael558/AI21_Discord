import scrapy
import warnings
import re

warnings.filterwarnings("ignore", message="Selector got both text and root, root is being ignored",
                        category=UserWarning)

REPLACE_PATTERN = re.compile('|'.join(map(re.escape, [' ', '​', ' ', ' ', '‍'])))

# â
def is_valid_text(text):
    text = REPLACE_PATTERN.sub(' ', text.strip())
    if ' ' not in text or len(text) > 1500:
        return None
    if text[0] == '"' and text[-1] == '"':
        text = text[1:-1]
    return text


def get_element_depth(element):
    return len(element.xpath('ancestor-or-self::node()'))


class AI21Spider(scrapy.Spider):
    name = "ai21_spider"
    allowed_domains = ['docs.ai21.com', 'ai21.com']
    start_urls = ['https://docs.ai21.com/docs/overview', 'https://www.ai21.com/']

    def parse(self, response):
        element_nodes = response.xpath('//*[not(self::script or self::style)]')
        for element in element_nodes:
            if element.xpath('ancestor::p'):
                continue

            if element.xpath('name()').get() == 'p':
                text_elements = element.xpath('string(.)')
            else:
                text_elements = element.xpath('text()[normalize-space()]')
            for text_element in text_elements:
                text = is_valid_text(text_element.get())
                if text:
                    depth = len(element.xpath('ancestor-or-self::node()'))
                    yield {'text': text, 'link': response.request.url, 'depth': depth}

        base_url = response.request.url.split('.com')[0] + '.com'
        for link in response.xpath('.//@href').getall():
            if link.endswith(".css"):
                continue
            if not link.startswith("https"):
                link = base_url + link
            yield response.follow(link, self.parse)
