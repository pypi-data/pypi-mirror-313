"""
Extract content from web page
"""
import requests
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
from requests.exceptions import RequestException
from langchain_community.document_loaders import AsyncChromiumLoader, AsyncHtmlLoader
from web_page_cls.utils.cleaner import delete_blank_lines, remove_urls

from enum import Enum


class HtmlScrapperMethod(Enum):
    """
    Methods for web html scrapping
    """
    REQUEST = 1  # simple request
    PLAYWRIGHT = 2  # langchain AsyncChromiumLoader
    AIOHTTP = 3  # langchain AsyncHtmlLoader


class ImageCleaner(MarkdownConverter):
    """
    Create a custom MarkdownConverter that del images
    """

    def convert_img(self, el, text, convert_as_inline):
        alt = el.attrs.get('alt', None) or ''
        src = el.attrs.get('src', None) or ''
        title = el.attrs.get('title', None) or ''
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''

        md_image_text = f'![{alt}]({src}{title_part})'
        # print(f'Delete image: {md_image_text}')

        return ""


def md_without_images(html, **options):
    return ImageCleaner(**options).convert(html)


def get_html_requests(url: str) -> str:
    """
    Extract content from web page
    """

    try:
        r = requests.get(url, timeout=10)
        return r.text
    except RequestException as e:
        print(f'Request exception for {url}: {e}')

    return ""


def get_html_playwright(url_str) -> str:
    """
    Get html with langchain AsyncChromiumLoader
    """
    loader = AsyncChromiumLoader([url_str])
    html = loader.load()
    return html[0].page_content


def get_html_aio(url_str) -> str:
    """
    Get html with langchain AsyncChromiumLoader
    """
    loader = AsyncHtmlLoader([url_str])
    html = loader.load()
    return html[0].page_content


def get_html(url: str, method: HtmlScrapperMethod = HtmlScrapperMethod.PLAYWRIGHT) -> str:
    """
    Extract content from web page
    """
    if method == HtmlScrapperMethod.REQUEST:
        return get_html_requests(url)
    elif method == HtmlScrapperMethod.AIOHTTP:
        return get_html_aio(url)

    # elif method == HtmlScrapperMethod.PLAYWRIGHT:
    return get_html_playwright(url)


def get_body(html):
    """
    Get body of web page
    """
    soup = BeautifulSoup(html, features="lxml")
    body = soup.find('body')
    if body is None:
        return soup.get_text()

    text = body.get_text()

    return text


def convert_html_to_md_without_images(html: str, skip_links=True) -> str:
    """
    html -> markdown
    """
    if skip_links:
        md_text = md_without_images(html, strip=['a'])
    else:
        md_text = md_without_images(html)

    md_text = delete_blank_lines(md_text)
    md_text = remove_urls(md_text)

    return md_text


if __name__ == '__main__':
    url_test = 'https://ria.ru/20240930/rossiya-1975421256.html'
    html_test = get_body(url_test)
    md_test = convert_html_to_md_with_vllm(html_test)
    print(md_test)
