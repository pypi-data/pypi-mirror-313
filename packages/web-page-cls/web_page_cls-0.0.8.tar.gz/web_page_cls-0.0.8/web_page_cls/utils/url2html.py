"""
Web Page Reader 
"""

from web_page_cls.utils.html2md import (convert_html_to_md_without_images,
                                        get_body, get_html, HtmlScrapperMethod)


def read_markdownify(url, method: HtmlScrapperMethod = HtmlScrapperMethod.AIOHTTP):
    """
    Read Web Page and convert to Markdown with markdownify package.
    """
    html = get_html(url, method=method)
    body = get_body(html)

    md = convert_html_to_md_without_images(body)

    return md
