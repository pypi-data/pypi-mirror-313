
"""
WebPage classifier with OpenAI server backend (vLLM)
"""
from web_page_cls.classifiers.classifier_base import WebPageClassifier
from web_page_cls.classifiers.config import WEB_PAGE_CLASSES

# pylint: disable=unsubscriptable-object


class WebPageClassifierStrictJsonOpenAI(WebPageClassifier):
    """
    Classifier of Web Page based on strictjson
    """

    def __init__(self, web_page_classes=WEB_PAGE_CLASSES, host="http://localhost:8000/v1", model="Qwen/Qwen2.5-3B-Instruct-AWQ") -> None:
        super().__init__(web_page_classes=web_page_classes, host=host, model=model)

    def llm(self, system_prompt: str, user_prompt: str) -> str:
        ''' Here, we use OpenAI for illustration, you can change it to your own LLM '''
        # ensure your LLM imports are all within this function
        from openai import OpenAI
        openai_api_key = "EMPTY"

        client = OpenAI(
            api_key=openai_api_key,
            base_url=self.host,
        )

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.6,
            top_p=0.9,
            max_tokens=256
        )
        return response.choices[0].message.content
