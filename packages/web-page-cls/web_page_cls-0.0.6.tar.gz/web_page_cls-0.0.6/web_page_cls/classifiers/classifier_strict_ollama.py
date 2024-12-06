
"""
WebPage classifier with Ollama backend
"""
from web_page_cls.classifiers.classifier_base import WebPageClassifier
from web_page_cls.classifiers.config import WEB_PAGE_CLASSES
# pylint: disable=unsubscriptable-object


class WebPageClassifierStrictJsonOllama(WebPageClassifier):
    """
    Classifier of Web Page based on strictjson
    """

    def __init__(self, web_page_classes=WEB_PAGE_CLASSES, host='http://localhost:11434', model='mistral-nemo') -> None:
        super().__init__(web_page_classes=web_page_classes, host=host, model=model)

    def llm(self, system_prompt: str, user_prompt: str) -> str:
        ''' Here, we use OpenAI for illustration, you can change it to your own LLM '''
        # ensure your LLM imports are all within this function
        from ollama import Client
        client = Client(host=self.host)

        # define your own LLM here
        response = client.chat(model=self.model, messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], options={'temperature': 0.3, 'num_predict': 128})
        return response['message']['content']
