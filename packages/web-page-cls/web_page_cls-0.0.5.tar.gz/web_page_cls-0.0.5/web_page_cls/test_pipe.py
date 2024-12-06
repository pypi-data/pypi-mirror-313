
import json

from colorama import Fore, Style
from colorama import init as colorama_init

from web_page_cls.classifiers.config import WEB_PAGE_CLASSES
from web_page_cls.pipeline import WebPagePipeline

colorama_init()


def test_url(url:str, fastetext_model_path:str):
    """
    Test one URL
    """

    pipeline = WebPagePipeline(fastetext_model_path=fastetext_model_path, model='mistral-nemo', web_page_classes=WEB_PAGE_CLASSES)


    print(
        f'\n{Fore.GREEN}Start pipeline: {Fore.YELLOW}{url}{Fore.WHITE}')

    pipe_results = pipeline.run_url(url)
    pipeline.print_pipe_results(pipe_results)

def test_html(html:str, fastetext_model_path:str):
    """
    Test one HTML
    """

    pipeline = WebPagePipeline(fastetext_model_path=fastetext_model_path, model='mistral-nemo', web_page_classes=WEB_PAGE_CLASSES)


    print(
        f'\n{Fore.GREEN}Start pipeline...')

    pipe_results = pipeline.run_html(html)
    pipeline.print_pipe_results(pipe_results)


def read_json(json_md_path: str) -> dict:
    """
    Load from JSON
    """

    with open(json_md_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(results, json_md_path: str) -> dict:
    """
    Save to JSON
    """

    with open(json_md_path, 'w', encoding='utf-8') as f:
        json.dump(results, f)

def is_content_valid(content:str):
    if '403 Forbidden' in content:
        return False
    
    if 'You do not have permission' in content:
        return False
    
    if 'Please recheck!' in content or 'Please check again' in content:
        return False
    
    if content == '':
        return False
    
    return True



def pipe_from_json(json_md_path: str, save_path: str, fastetext_model_path: str, model='mistral-nemo'):
    """
    Run pipeline from JSON crawler
    """

    md_data = read_json(json_md_path)

    pipeline = WebPagePipeline(web_page_classes=WEB_PAGE_CLASSES, fastetext_model_path=fastetext_model_path, model=model)

    results = {}

    content_size = sum(len(md_data[url])  for url in md_data)
    tek_suburl = 0

    for url in md_data:

        subres = {}
        for sub_url, content_md in md_data[url].items():

            if not is_content_valid(content_md):
                tek_suburl += 1
                continue

            print(
                f'\n{Fore.GREEN}{tek_suburl+1}/{content_size} Start pipeline: {Fore.YELLOW}{sub_url}{Fore.WHITE}')

            pipe_results = pipeline.run_md(content_md)
            pipeline.print_pipe_results(pipe_results)

            subres[sub_url] = pipe_results
            tek_suburl += 1
            
        if len(subres):
            results[url] = subres

    save_json(results, save_path)


if __name__ == '__main__':

    fastetext_model_path="/home/roman/py_projects/offensive_ai/lid.176.bin"
    url = "https://proglib.io/p/kak-opublikovat-svoyu-python-biblioteku-na-pypi-2020-01-28"

    test_html_path = '/home/roman/py_projects/offensive_ai/web_page_cls/test.html'
    with open(test_html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # test_url(url=url, fastetext_model_path=fastetext_model_path)
    test_html(html=html, fastetext_model_path=fastetext_model_path)

    # pipe_from_json('/home/roman/py_projects/offensive_ai/web_page_cls/dom_urls_content.json', 'dom_result_qwen2.5.json', fastetext_model_path = fastetext_model_path, model='qwen2.5')