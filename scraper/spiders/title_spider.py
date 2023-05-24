import re
import string
import scrapy
from bs4 import BeautifulSoup

REPLACE_CODE_PATTERN = re.compile('|'.join(map(re.escape, [' ', '​', ' ', ' ', '‍'])))
CHARACTER_LIMIT = 2000


def has_punctuation(input_string):
    for char in input_string:
        if char in string.punctuation:
            return True
    return False


def extract_text_nodes(soup):
    text_nodes = dict()
    index = 0  # for ordering

    pre_punctuation = False
    post_punctuation_index = 0
    for strng in soup.stripped_strings:
        if len(strng) > CHARACTER_LIMIT:
            strng = strng[:CHARACTER_LIMIT].strip() + '\n...Text Truncated...\n'

        if has_punctuation(strng):
            pre_punctuation = True
            post_punctuation_index = index

        if pre_punctuation:  # ignore navigation links at the beginning
            text_nodes[strng] = index
            index += 1

    text_nodes = sorted(text_nodes.items(), key=lambda x: x[1])
    text_nodes = text_nodes[:post_punctuation_index + 1]  # ignore navigation links at the end

    return '\n'.join(text for text, _ in text_nodes)


def innertext(body):
    soup = BeautifulSoup(body, 'html.parser')

    # Remove CSS and JavaScript tags from the parsed HTML
    for css_tag in soup.select('style'):
        css_tag.decompose()
    for js_tag in soup.select('script'):
        js_tag.decompose()

    return extract_text_nodes(soup)


def clean_text(text):
    text = REPLACE_CODE_PATTERN.sub(' ', text.strip())
    return text


class AI21Spider(scrapy.Spider):
    name = "ai21_spider"
    allowed_domains = ['docs.ai21.com', 'ai21.com']
    start_urls = ['https://docs.ai21.com/docs/overview', 'https://www.ai21.com/']

    def parse(self, response):
        # Extract the title using an XPath selector
        title = response.xpath('//title/text()').get()
        page_text = innertext(response.body)
        page_text = clean_text(page_text)

        if title and page_text:
            yield {'title': title, 'text': page_text, 'link': response.request.url}

        base_url = response.request.url.split('.com')[0] + '.com'
        for link in response.xpath('.//@href').getall():
            if link.endswith(".css") or link.endswith(".js") or link.startswith("#") or "status.ai21.com" in link:
                continue
            if not link.startswith("https"):
                link = base_url + link

            yield response.follow(link, self.parse)
