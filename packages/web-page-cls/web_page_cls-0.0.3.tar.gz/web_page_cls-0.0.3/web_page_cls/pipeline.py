"""
Base web page processing pipeline,
includes classification, annotation 
and language identification
"""
from colorama import Fore, Style
from colorama import init as colorama_init

from web_page_cls.annotator import annotate
from web_page_cls.classifiers.classifier_simple import WebPageClassifierSimple
from web_page_cls.classifiers.classifier_strict_ollama import \
    WebPageClassifierStrictJsonOllama
from web_page_cls.classifiers.config import WEB_PAGE_CLASSES
from web_page_cls.lang_detectors.lang_detector import LanguageIdentificator
from web_page_cls.utils.html2md import convert_html_to_md_without_images
from web_page_cls.utils.url2html import read_markdownify

colorama_init()


class WebPagePipeline:
    """
    Base web page processing pipeline,
    includes classification, annotation 
    and language identification
    """

    def __init__(self, fastetext_model_path: str, model='mistral-nemo', web_page_classes=WEB_PAGE_CLASSES,
                 ollama_host='http://localhost:11434', use_cls_strict=True) -> None:

        self.lang_detector = LanguageIdentificator(
            model_path=fastetext_model_path)
        self.model = model
        self.ollama_host = ollama_host
        self.web_page_classes = web_page_classes

        if use_cls_strict:
            self.classificator = WebPageClassifierStrictJsonOllama(web_page_classes=self.web_page_classes,
                                                                   host=ollama_host, model=model)
        else:
            self.classificator = WebPageClassifierSimple(web_page_classes=self.web_page_classes,
                                                         ollama_host=ollama_host, ollama_model=model)

    def run_url(self, url: str):
        """
        Pipeline of web page processing
        """

        web_page_md = read_markdownify(url)

        return self.run_md(web_page_md)

    def run_html(self, html: str):
        """
        Run pipe with html
        """
        md = convert_html_to_md_without_images(html)

        return self.run_md(md)

    def run_md(self, web_page_md: str):
        """
        Run pipe with md text
        """

        results = {'content': web_page_md}

        results['lang'] = self.lang_detector.predict(web_page_md)

        results['classification'] = self.classificator.predict(web_page_md)

        results['annotation'] = annotate(
            web_page_md, model=self.model, ollama_host=self.ollama_host)

        return results

    def print_pipe_results(self, results):
        """
        results: dict {'lang': {'label': str,
                                'prob': str}, 
                    'classification': str,
                    'annotation': str}
        """

        print(f'\n{Fore.GREEN}RESULTS:')
        lang_str = f'{Fore.YELLOW}lang: {Fore.WHITE}{results["lang"]["label"]}'
        prob_str = f'{Fore.YELLOW}prob: {Fore.WHITE}{results["lang"]["prob"]:0.3f}'
        print(
            f'{lang_str} {prob_str}')
        print(
            f'{Fore.YELLOW}classification: {Fore.WHITE}{results["classification"]}')
        print(f'{Fore.YELLOW}annotation: {Fore.WHITE}{results["annotation"]}')
