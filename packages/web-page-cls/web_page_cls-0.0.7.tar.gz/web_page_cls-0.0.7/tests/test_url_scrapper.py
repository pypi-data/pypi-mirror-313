from web_page_cls.utils.url2html import get_html, read_markdownify, HtmlScrapperMethod

URL = 'https://connectaman.hashnode.dev/top-100-nlp-interview-question'


def test_langchain_html():
    """
    Test langchain html extraction
    """

    print(get_html(URL, method=HtmlScrapperMethod.AIOHTTP))


def test_md():
    """
    Test url -> md pipeline
    """

    print(read_markdownify(URL))


if __name__ == '__main__':

    test_md()
