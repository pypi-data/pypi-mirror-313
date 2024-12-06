"""
Web Page Classifier Simple version
"""
# pylint: disable=unsubscriptable-object
import json

import ollama
from ollama import Client

from web_page_cls.classifiers.cls_prompts import web_page_classify_template
from web_page_cls.utils.chunker import ChunkerMistral


class WebPageClassifierSimple:
    """
    Classifier of Web Page based
    """

    def __init__(self, web_page_classes, ollama_host='http://localhost:11434', ollama_model='mistral-nemo', chunk_size=4000) -> None:
        self.model = ollama_model
        self.host = ollama_host
        self.web_page_classes = web_page_classes
        self.chunker = ChunkerMistral()
        self.chunk_size = chunk_size

    def predict_one_chunk(self, web_page_md: str):
        """
        Classify web page
        """

        web_page_cls_str = ', '.join(list(self.web_page_classes.values()))
        prompt = web_page_classify_template.substitute(
            {'content': web_page_md,
             'web_page_classes': web_page_cls_str.lower()})

        client = Client(host=self.host)
        response = client.chat(model=self.model, messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])

        return response['message']['content']

    def convert_to_json(self, results: str):

        if results.startswith('```json'):
            results = results.replace('```json', '')
            results = results.replace('```', '')
        try:
            return json.loads(results)
        except Exception as e:
            print(e)
            return None

    def update_label(self, label, labels)->dict:
        if label == '':
            return labels
        label = label.lower().strip()
        if ',' in label:
            labels_list = label.split(',')
            labels = self.update_labels_if_list(labels_list, labels)
        elif '_' in label:
            label = label.replace('_', ' ')
            labels[label] = labels.get(label, 0) + 1
        else:
            labels[label] = labels.get(label, 0) + 1
        
        return labels


    def update_labels_if_dict(self, labels_pred_json, labels: dict) -> dict:
        for _, label in labels_pred_json.items():
            labels = self.update_labels(label, labels)

        return labels

    def update_labels_if_list(self, labels_pred_json, labels: dict) -> dict:
        for label in labels_pred_json:
            labels = self.update_labels(label, labels)
        return labels

    def update_labels(self, labels_pred_json, labels: dict) -> dict:

        if not labels_pred_json:
            return labels
        
        if isinstance(labels_pred_json, dict):
            return self.update_labels_if_dict(labels_pred_json, labels)
        if isinstance(labels_pred_json, list):
            return self.update_labels_if_list(labels_pred_json, labels)
        elif isinstance(labels_pred_json, str):
            return self.update_label(labels_pred_json, labels)

        return labels

    def predict(self, web_page_md: str) -> dict:
        """
        Use strictjson to validate LLM outputs

        Returns dict 
        {
            "Class1": <chunks count>,
            "Class2": <chunks count>,
        }
        """
        labels = {}
        for chunk in self.chunker.chunk(content=web_page_md, chunk_max_tokens=self.chunk_size):

            labels_pred = self.predict_one_chunk(chunk)

            labels_pred_json = self.convert_to_json(labels_pred)

            labels = self.update_labels(labels_pred_json, labels)

        return labels

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
