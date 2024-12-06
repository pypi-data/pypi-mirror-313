import csv
import os
import json

from dataclasses import dataclass
import dataclasses

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()


@dataclass
class WebSiteRecord:
    """
    Sample of Website Classification dataset from
    https://www.kaggle.com/datasets/hetulmehta/website-classification?resource=download
    """
    id: int
    website_url: str
    cleaned_website_text: str
    label: str


class EnhancedJSONEncoder(json.JSONEncoder):
    """
    Support convert dataclass to JSON
    """

    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


ds_path = os.path.join(os.path.dirname(__file__), 'website_classification.csv')

headers = ['#', 'website_url', 'cleaned_website_text', 'Category']


class WebPagesDataset:
    """
    Website Classification dataset from
    https://www.kaggle.com/datasets/hetulmehta/website-classification?resource=download
    """

    def __init__(self, csv_path=ds_path) -> None:

        self.csv_path = csv_path
        self.json_path = os.path.join(os.path.dirname(
            __file__), 'website_classification.json')

        self.json_data = []

        self.labels = ['Forums', 'Streaming Services', 'Photography', 'Travel', 'Computers and Technology', 'E-Commerce', 'Adult', 'Health and Fitness',
                       'Education', 'Games', 'Social Networking and Messaging', 'Sports', 'Business/Corporate', 'Food', 'Law and Government', 'News']

        self.id2label = {0: 'Forums', 1: 'Streaming Services', 2: 'Photography', 3: 'Travel', 4: 'Computers and Technology', 5: 'E-Commerce', 6: 'Adult', 7: 'Health and Fitness',
                         8: 'Education', 9: 'Games', 10: 'Social Networking and Messaging', 11: 'Sports', 12: 'Business/Corporate', 13: 'Food', 14: 'Law and Government', 15: 'News'}

        self.label2id = {k: v for v, k in self.id2label.items()}

        if not os.path.exists(csv_path):
            print(
                f'{Fore.RED}Error: csv file {csv_path} not exists {Style.RESET_ALL}')
            return

        if not os.path.exists(self.json_path):
            self.csv2json()
        else:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.json_data = json.load(f)

    def csv2json(self):
        """
        Convert dataset from csv to json
        """

        self.json_data = []
        labels = set()

        with open(self.csv_path, 'r', encoding='utf-8') as csvfile:

            print(
                f'{Fore.CYAN}Start Website Classification dataset csv->json converter...')
            spamreader = csv.reader(csvfile, delimiter=',')

            for i, row in enumerate(spamreader):

                if i == 0:
                    continue  # header

                record = WebSiteRecord(
                    id=row[0], website_url=row[1], cleaned_website_text=row[2], label=row[3])
                self.json_data.append(record)
                labels.add(row[3])

        print(f'{Fore.CYAN}Start Website Classification dataset csv->json converter...')

        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(self.json_data, f, ensure_ascii=False,
                      cls=EnhancedJSONEncoder)

        print(f'{Fore.CYAN}Dataset saved at: {Fore.YELLOW}{self.json_path}')
        print(f'{Fore.MAGENTA}Labels {len(labels)}: {Fore.YELLOW}{labels}')
        print(f'{Fore.MAGENTA}Records total: {Fore.YELLOW}{len(self.json_data)}')

        assert labels == set(self.labels)


if __name__ == '__main__':

    ds = WebPagesDataset()

    print(f'{Fore.MAGENTA}Labels {len(ds.labels)}: {Fore.YELLOW}{ds.labels}')
    print(f'{Fore.MAGENTA}Records total: {Fore.YELLOW}{len(ds.json_data)}')
