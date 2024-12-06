"""
Extract content from web page
"""
import requests
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
from requests.exceptions import RequestException

from web_page_cls.utils.cleaner import delete_blank_lines, remove_urls
from web_page_cls.utils.image_cache_handler import dump_cache, read_cache
from web_page_cls.utils.vllm_image import vllm_pipeline


class ImageVLLMConverter(MarkdownConverter):
    """
    Create a custom MarkdownConverter that use VLLM to understand image
    """

    def __init__(self, prompt="What is in this picture?",
                 model="llava",
                 ollama_host="http://localhost:11434", **options):
        super().__init__(**options)

        self.prompt = prompt
        self.model = model
        self.ollama_host = ollama_host
        self.image_cache = read_cache()

    def convert_img(self, el, text, convert_as_inline):
        src = el.attrs.get('src', None) or ''

        if src in self.image_cache:

            print(f"Found {src} in cache... ")

            return self.image_cache[src]

        text_from_image = vllm_pipeline(src,
                                        prompt=self.prompt,
                                        model=self.model,
                                        ollama_host=self.ollama_host)

        if text_from_image:
            md_image_text = f'The picture shows: {text_from_image}'
        else:
            md_image_text = ""

        self.image_cache[src] = md_image_text

        dump_cache(self.image_cache)

        return md_image_text


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


def md_with_vllm(html, prompt="What is in this picture?",
                 model="llava",
                 ollama_host="http://localhost:11434", **options):
    return ImageVLLMConverter(prompt=prompt, model=model, ollama_host=ollama_host, **options).convert(html)


def md_without_images(html, **options):
    return ImageCleaner(**options).convert(html)


def get_html(url: str) -> str:
    """
    Extract content from web page
    """
    try:
        r = requests.get(url, timeout=10)
        return r.text
    except RequestException as e:
        print(f'Request exception for {url}: {e}')

    return ""


def get_body(html):
    """
    Get body of web page
    """
    soup = BeautifulSoup(html)
    body = soup.find('body')
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


def convert_html_to_md_with_vllm(html: str, skip_links=True,
                                 prompt="What is in this picture?",
                                 model="llava",
                                 ollama_host="http://localhost:11434") -> str:
    """
    html -> markdown
    """
    if skip_links:
        md_text = md_with_vllm(
            html, prompt=prompt, model=model, ollama_host=ollama_host, strip=['a'])
    else:
        md_text = md_with_vllm(html, prompt=prompt,
                               model=model, ollama_host=ollama_host)

    md_text = delete_blank_lines(md_text)
    md_text = remove_urls(md_text)

    return md_text


if __name__ == '__main__':
    url_test = 'https://ria.ru/20240930/rossiya-1975421256.html'
    html_test = get_body(url_test)
    md_test = convert_html_to_md_with_vllm(html_test)
    print(md_test)
