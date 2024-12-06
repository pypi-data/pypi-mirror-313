"""
Web Page Classifier Simple version
"""
import ollama
from ollama import Client

from web_page_cls.classifiers.cls_prompts import web_page_classify_template


# pylint: disable=unsubscriptable-object


class WebPageClassifierSimple:
    """
    Classifier of Web Page based
    """

    def __init__(self, web_page_classes, ollama_host='http://localhost:11434', ollama_model='mistral-nemo') -> None:
        self.model = ollama_model
        self.host = ollama_host
        self.web_page_classes = web_page_classes

    def predict(self, web_page_md: str):
        """
        Classify web page
        """

        web_page_cls_str = ', '.join(list(self.web_page_classes.values()))
        prompt = web_page_classify_template.substitute(
            {'content': web_page_md,
             'web_page_classes': web_page_cls_str})

        client = Client(host=self.host)
        response = client.chat(model=self.model, messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])

        return response['message']['content']

    def predict_stream(self, web_page_md: str):
        """
        Classify web page and print in stream 
        """

        web_page_cls_str = ', '.join(list(self.web_page_classes.values()))
        prompt = web_page_classify_template.substitute(
            {'content': web_page_md,
             'web_page_classes': web_page_cls_str})

        stream = ollama.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}],
            stream=True,
        )

        for chunk in stream:
            print(chunk['message']['content'], end='', flush=True)


if __name__ == '__main__':
    from colorama import Fore, Style
    from colorama import init as colorama_init
    from web_page_cls.classifiers.config import WEB_PAGE_CLASSES

    from web_page_cls.datasets.dataset_reader import WebPagesDataset
    from web_page_cls.utils.url2html import read_markdownify

    colorama_init()

    ds = WebPagesDataset()

    FROM_URLS = False

    classifier = WebPageClassifierSimple(web_page_classes=WEB_PAGE_CLASSES)

    print(f'{Fore.MAGENTA}Labels {len(ds.labels)}: {Fore.YELLOW}{ds.labels}')
    print(f'{Fore.MAGENTA}Records total: {Fore.YELLOW}{len(ds.json_data)}{Style.RESET_ALL}')

    test_data = {}
    for lbl in ds.labels:
        test_data[lbl] = [
            record for record in ds.json_data if record['label'] == lbl][:10]

    for true_label, records in test_data.items():

        for record in records:

            if FROM_URLS:
                content = read_markdownify(record['website_url'])
            else:
                content = record['cleaned_website_text']

            print(
                f'\n{Fore.GREEN}Start classification: {Fore.YELLOW}{record["website_url"]}{Fore.WHITE}')

            print(classifier.predict(content))

            print(f'\n{Fore.MAGENTA}Real label: {Fore.YELLOW}{true_label}')
