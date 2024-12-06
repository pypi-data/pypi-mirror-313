import os
from collections import OrderedDict
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "requirements.txt")) as f:
    dependencies = f.read().strip().split("\n")

setup(
    name="web_page_cls",
    version="0.0.1",
    description="Web page LLM classifier and summarizer",
    long_description="A web-based language model (LLM) classifier and summarizer is a comprehensive tool designed to process and analyze text data on the internet. This system leverages advanced natural language processing (NLP) techniques to classify and summarize various types of content efficiently",
    long_description_content_type='text/x-rst',
    author="Jack",
    author_email="jack@ntu.edu.sg",
    url="",
    license="MIT License",
    packages=find_packages(),
    install_requires=dependencies,
    # package_data={'': ['*.bin', '*.tab']}
)
