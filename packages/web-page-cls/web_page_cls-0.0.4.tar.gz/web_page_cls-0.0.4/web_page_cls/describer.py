"""
Web Page Describer
"""
import ollama
from ollama import Client

from web_page_cls.utils.prompts import web_page_what_a_page_template

# pylint: disable=unsubscriptable-object


def describe(web_page_md: str, model='qwen2.5', ollama_host='http://localhost:11434'):
    """
    Describe web page
    """

    prompt = web_page_what_a_page_template.substitute({'content': web_page_md})

    client = Client(host=ollama_host)
    response = client.chat(model=model, messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])

    return response['message']['content']


def describe_stream(web_page_md: str, model='qwen2.5'):
    """
    Describe web page in stream
    """

    prompt = web_page_what_a_page_template.substitute({'content': web_page_md})

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
    from utils.url2html import read_markdownify

    colorama_init()

    ds = WebPagesDataset()

    FROM_URLS = True

    print(f'{Fore.MAGENTA}Labels {len(ds.labels)}: {Fore.YELLOW}{ds.labels}')
    print(f'{Fore.MAGENTA}Records total: {Fore.YELLOW}{len(ds.json_data)}{Style.RESET_ALL}')

    test_data = {}
    for lbl in ds.labels:
        test_data[lbl] = [
            record for record in ds.json_data if record['label'] == lbl][:10]

    # content = read_reader_lm(url_test)

    for true_label, records in test_data.items():

        for record in records:

            if FROM_URLS:
                content = read_markdownify(record['website_url'])
            else:
                content = record['cleaned_website_text']
            # content = delete_unrelative_info(content, model = 'llama3.1')

            print(
                f'\n{Fore.GREEN}Start classification: {Fore.YELLOW}{record["website_url"]}{Fore.WHITE}')

            describe(content, model='mistral-nemo')

            print(
                f'\n{Fore.GREEN}Real cleaned website text {Fore.YELLOW}{record["cleaned_website_text"]}')
