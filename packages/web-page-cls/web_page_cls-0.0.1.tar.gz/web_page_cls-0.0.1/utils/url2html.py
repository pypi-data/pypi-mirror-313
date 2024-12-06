"""
Web Page Reader 
"""
from ollama import Client

from utils.html2md import (
    convert_html_to_md_with_vllm,
    convert_html_to_md_without_images,
    get_body,
    get_html,
)


def read_markdownify_with_images(url,
                                 prompt="What is in this picture?",
                                 model="llava",
                                 ollama_host="http://localhost:11434"):
    """
    Read Web Page and convert to Markdown with markdownify package.
    Use VLLM from Ollama for images understanding
    """
    html = get_html(url)
    # body = get_body(html)

    md = convert_html_to_md_with_vllm(
        html, prompt=prompt, model=model, ollama_host=ollama_host)
    return md


def read_markdownify(url):
    """
    Read Web Page and convert to Markdown with markdownify package.
    """
    html = get_html(url)
    # body = get_body(html)

    md = convert_html_to_md_without_images(html)

    return md


def read_reader_lm(url,
                   model="reader-lm",
                   ollama_host="http://localhost:11434"):
    """
    Use Ollama Reader-LM model to convert html to markdown
    """

    html = get_html(url)
    # body = get_body(html)

    client = Client(host=ollama_host)
    response = client.chat(model=model, messages=[
        {
            'role': 'user',
            'content': html,
        },
    ])

    return response['message']['content']
