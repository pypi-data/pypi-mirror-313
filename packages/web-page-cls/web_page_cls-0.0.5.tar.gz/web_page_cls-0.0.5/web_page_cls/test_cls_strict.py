import os
import time

from colorama import Fore, Style
from colorama import init as colorama_init

from web_page_cls.classifiers.classifier_strict_ollama import \
    WebPageClassifierStrictJsonOllama
from web_page_cls.classifiers.classifier_strict_openai import \
    WebPageClassifierStrictJsonOpenAI
from datasets.dataset_reader import WebPagesDataset
from web_page_cls.utils.metrics import LLMMetrics
from web_page_cls.utils.url2html import read_markdownify

colorama_init()

ds = WebPagesDataset()

FROM_URLS = False
LABELS_PER_CLASS = 10
MODEL_NAME = 'granite3-dense:8b' #'hermes3:latest'  # 'llama3.1'

classifier = WebPageClassifierStrictJsonOllama(model=MODEL_NAME)

metrics = LLMMetrics(ds.labels)

print(f'{Fore.MAGENTA}Labels {len(ds.labels)}: {Fore.YELLOW}{ds.labels}')
print(f'{Fore.MAGENTA}Records total: {Fore.YELLOW}{len(ds.json_data)}{Style.RESET_ALL}')


test_data = {}
for lbl in ds.labels:
    test_data[lbl] = [
        record for record in ds.json_data if record['label'] == lbl][:LABELS_PER_CLASS]

start_test = time.time()

total_examples = LABELS_PER_CLASS * len(ds.labels)
tek_example = 0

for true_label, records in test_data.items():

    for record in records:

        if FROM_URLS:
            content = read_markdownify(record['website_url'])
        else:
            content = record['cleaned_website_text']

        rec_wrapper_str = f'{Fore.YELLOW}{record["website_url"]}{Fore.WHITE}'

        print(
            f'\n{Fore.GREEN}Classify {tek_example + 1}/{total_examples}: {rec_wrapper_str}')

        pred = classifier.predict(content)
        print(pred)
        print(f'{Fore.MAGENTA}Real label: {Fore.YELLOW}{true_label}')

        if "label" in pred:
            metrics.add_llm_strict_output_and_true_value(
                pred["label"], true_label)
        else:
            metrics.add_llm_strict_output_and_true_value([], true_label)

        print(metrics.get_report())

        tek_example += 1

test_time = time.time() - start_test
print(f'{Fore.GREEN}Total test time: {Fore.YELLOW}{test_time: 0.3f} sec')
print(f'{Fore.GREEN}Example mean process time: {Fore.YELLOW}{test_time/total_examples: 0.3f} sec')
print(f'{Fore.RED}REPORT:{Fore.WHITE}')
print(metrics.get_report())
metrics.save_confusion_matrix(os.path.join(os.path.dirname(
    __file__), 'results', f'confusion_matrix_{MODEL_NAME}.png'))
