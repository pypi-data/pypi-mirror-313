import os
from collections import OrderedDict
from setuptools import find_packages, setup

# with open(os.path.join(os.path.dirname(__file__), "requirements.txt")) as f:
#     dependencies = f.read().strip().split("\n")

dependencies = ['annotated-types==0.7.0', 'anyio==4.6.2.post1', 'asyncio==3.4.3', 'beautifulsoup4==4.12.3', 'certifi==2024.8.30', 'charset-normalizer==3.4.0', 'colorama==0.4.6', 'contourpy==1.3.0', 'cycler==0.12.1', 'distro==1.9.0', 'exceptiongroup==1.2.2', 'fasttext==0.9.3', 'filelock==3.16.1', 'fonttools==4.54.1', 'fsspec==2024.9.0', 'h11==0.14.0', 'httpcore==1.0.6', 'httpx==0.27.2', 'huggingface-hub==0.25.2', 'idna==3.10', 'jiter==0.6.1', 'joblib==1.4.2', 'kiwisolver==1.4.7', 'lxml==5.3.0', 'markdownify==0.13.1', 'matplotlib==3.9.2', 'numpy==2.1.2', 'ollama==0.3.3', 'openai==1.51.2', 'packaging==24.1', 'pandas==2.2.3', 'pillow==10.4.0', 'pybind11==2.13.6', 'pydantic==2.9.2', 'pydantic_core==2.23.4', 'pyparsing==3.2.0', 'python-dateutil==2.9.0.post0', 'python-docx==1.1.2', 'pytz==2024.2', 'PyYAML==6.0.2', 'requests==2.32.3', 'scikit-learn==1.5.2', 'scipy==1.14.1', 'seaborn==0.13.2', 'six==1.16.0', 'sniffio==1.3.1', 'soupsieve==2.6', 'strictjson==5.1.3', 'threadpoolctl==3.5.0', 'tqdm==4.66.5', 'typing_extensions==4.12.2', 'tzdata==2024.2', 'urllib3==2.2.3']

setup(
    name="web_page_cls",
    version="0.0.3",
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
