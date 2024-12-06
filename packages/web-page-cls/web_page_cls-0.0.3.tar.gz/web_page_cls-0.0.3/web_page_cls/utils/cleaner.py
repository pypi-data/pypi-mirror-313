"""
Clean and Prettify Text Utils
"""
import re

import ollama

from utils.prompts import clean_prompt_template


def delete_unrelative_info(web_page_md: str, model='qwen2.5'):
    """
    Delete unrelative info from site
    """

    prompt = clean_prompt_template.substitute({'content': web_page_md})

    response = ollama.chat(model=model, messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    return response['message']['content']


def delete_blank_lines(text: str) -> str:
    """
    Delete blank lines from text 
    """
    lines = [line for line in text.split('\n') if line.strip() != ""]

    return '\n'.join(lines)


def remove_urls(text, replacement_text=""):
    """
    Remove url from text
    """
    # Define a regex pattern to match URLs
    url_pattern = re.compile(r'https?://\S+|www\.\S+')

    # Use the sub() method to replace URLs with the specified replacement text
    text_without_urls = url_pattern.sub(replacement_text, text)

    return text_without_urls

