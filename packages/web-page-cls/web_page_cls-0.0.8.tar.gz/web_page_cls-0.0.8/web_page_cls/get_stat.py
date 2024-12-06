import os
import json

from web_page_cls.utils.io import read_json, save_json
import matplotlib.pyplot as plt

iso2lang = read_json('lang_detectors/code2lang.json')


def plot_pie(labels_with_values:dict, title, savepath):
    """
    Plotting the pie chart
    """
    labels, counts = list(labels_with_values.keys()), list(labels_with_values.values())
    plt.figure(figsize=(12, 8))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(title)
    plt.savefig(savepath, dpi=600)

def print_stat(filepath:str):

    """
    "content": "Temporarily Unavailable.",
            "lang": {
                "label": "en",
                "prob": 0.40031716227531433
            },
            "classification": {
                "label": "Bad request"
            },
            "annotation": "The webpage is currently unavailable."
    """

    results = read_json(filepath)

    labels = {}
    langs = {}
    urls_count = 0

    for url in results:
        for sub_url, result in results[url].items():
            if result['content'] == "":
                continue
            lang = result['lang']['label'].lower()
            lang = iso2lang[lang]
    
            if lang not in langs:
                langs[lang] = 1
            else:
                langs[lang] += 1

            label = result['classification'].get('label', '').lower()
            if label == '':
                continue
            if label not in labels:
                labels[label] = 1
            else:
                labels[label] += 1

            urls_count += 1

    print(f'Langs: {langs}')
    print(f'Labels: {labels}')
    print(f'Total urls: {urls_count}')

    plot_pie(labels_with_values=labels, title='Labels', savepath='labels.png')
    plot_pie(labels_with_values=langs, title='Langs', savepath='langs.png')

if __name__ == '__main__':

    print_stat('dom_result_qwen2.5.json')

            




