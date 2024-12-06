"""
Web Page Annotator
"""
import ollama
from ollama import Client

from web_page_cls.utils.prompts import web_page_annotate_template

# pylint: disable=unsubscriptable-object


def annotate(web_page_md: str, model='qwen2.5', ollama_host='http://localhost:11434'):
    """
    Annotate web page
    """

    prompt = web_page_annotate_template.substitute(
        {'content': web_page_md})

    client = Client(host=ollama_host)
    response = client.chat(model=model, messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])

    return response['message']['content']


def annotate_stream(web_page_md: str, model='qwen2.5'):
    """
    Annotate web page in stream
    """

    prompt = web_page_annotate_template.substitute(
        {'content': web_page_md})

    stream = ollama.chat(
        model=model,
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
    )

    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)


if __name__ == '__main__':
    from colorama import Fore, Style
    from colorama import init as colorama_init

    from datasets.dataset_reader import WebPagesDataset
    from web_page_cls.utils.url2html import read_markdownify

    colorama_init()

    ds = WebPagesDataset()

    FROM_URLS = False

    print(f'{Fore.MAGENTA}Labels {len(ds.labels)}: {Fore.YELLOW}{ds.labels}')
    print(f'{Fore.MAGENTA}Records total: {Fore.YELLOW}{len(ds.json_data)}{Style.RESET_ALL}')

    test_data = {}
    for lbl in ds.labels:
        test_data[lbl] = [
            record for record in ds.json_data if record['label'] == lbl][:3]

    for true_label, records in test_data.items():

        for record in records:

            if FROM_URLS:
                content = read_markdownify(record['website_url'])
            else:
                content = record['cleaned_website_text']

            print(
                f'\n{Fore.GREEN}Start classification: {Fore.YELLOW}{record["website_url"]}{Fore.WHITE}')

            annotate_stream(content, model='mistral-nemo')

            print(
                f'\n{Fore.GREEN}Real cleaned website text {Fore.YELLOW}{record["cleaned_website_text"]}')
