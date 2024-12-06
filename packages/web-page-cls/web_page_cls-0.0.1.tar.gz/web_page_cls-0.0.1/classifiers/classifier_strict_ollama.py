
"""
WebPage classifier with Ollama backend
"""
from classifiers.classifier_base import WebPageClassifier

# pylint: disable=unsubscriptable-object


class WebPageClassifierStrictJsonOllama(WebPageClassifier):
    """
    Classifier of Web Page based on strictjson
    """

    def __init__(self, host='http://localhost:11434', model='mistral-nemo') -> None:
        self.model = model
        self.host = host

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
