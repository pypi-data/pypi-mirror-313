from colorama import Fore, Style
from colorama import init as colorama_init

from datasets.dataset_reader import WebPagesDataset
from web_page_cls.utils.url2html import read_markdownify
from web_page_cls.classifiers.classifier_simple import WebPageClassifierSimple

colorama_init()

ds = WebPagesDataset()

FROM_URLS = False

classifier = WebPageClassifierSimple()

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