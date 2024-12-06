"""
Setup for Web Page Classificator
"""
from setuptools import find_packages, setup
# import os
# with open(os.path.join(os.path.dirname(__file__), "requirements.txt")) as f:
#     dependencies = f.read().strip().split("\n")

dependencies = ['annotated-types==0.7.0', 'anyio==4.6.2.post1', 'asyncio==3.4.3', 'beautifulsoup4==4.12.3',
                'certifi==2024.8.30', 'charset-normalizer==3.4.0', 'colorama==0.4.6', 'contourpy==1.3.0',
                'cycler==0.12.1', 'distro==1.9.0', 'exceptiongroup==1.2.2', 'fasttext==0.9.3', 'filelock==3.16.1',
                'fonttools==4.54.1', 'fsspec==2024.9.0', 'h11==0.14.0', 'httpcore==1.0.6', 'httpx==0.27.2',
                'huggingface-hub==0.25.2', 'idna==3.10', 'jiter==0.6.1', 'joblib==1.4.2', 'kiwisolver==1.4.7',
                'lxml==5.3.0', 'markdownify==0.13.1', 'matplotlib==3.9.2', 'numpy', 'ollama==0.3.3',
                'packaging==24.1', 'pandas==2.2.3', 'pillow==10.4.0', 'pybind11==2.13.6', 'pydantic==2.9.2', 'pydantic_core==2.23.4', 'pyparsing==3.2.0', 'python-dateutil==2.9.0.post0', 'python-docx==1.1.2', 'pytz==2024.2', 'PyYAML==6.0.2', 'requests==2.32.3', 'scikit-learn==1.5.2', 'scipy==1.14.1', 'seaborn==0.13.2', 'six==1.16.0', 'sniffio==1.3.1', 'soupsieve==2.6', 'strictjson==5.1.3', 'threadpoolctl==3.5.0', 'tqdm==4.66.5', 'typing_extensions==4.12.2', 'tzdata==2024.2', 'urllib3==2.2.3', 'aiohappyeyeballs==2.4.4', 'aiohttp==3.11.9', 'aiosignal==1.3.1', 'annotated-types==0.7.0', 'anyio==4.6.2.post1', 'async-timeout==4.0.3', 'asyncio==3.4.3', 'attrs==24.2.0', 'backports.tarfile==1.2.0', 'beautifulsoup4==4.12.3', 'certifi==2024.8.30', 'cffi==1.17.1', 'charset-normalizer==3.4.0', 'colorama==0.4.6', 'contourpy==1.3.0', 'cryptography==44.0.0', 'cycler==0.12.1', 'dataclasses-json==0.6.7', 'distro==1.9.0', 'docutils==0.21.2', 'exceptiongroup==1.2.2', 'fasttext==0.9.3', 'filelock==3.16.1', 'fonttools==4.54.1', 'frozenlist==1.5.0', 'fsspec==2024.9.0', 'greenlet==3.1.1', 'h11==0.14.0', 'httpcore==1.0.6', 'httpx==0.27.2', 'httpx-sse==0.4.0', 'huggingface-hub==0.25.2', 'idna==3.10', 'importlib_metadata==8.5.0', 'jaraco.classes==3.4.0', 'jaraco.context==6.0.1', 'jaraco.functools==4.1.0', 'jeepney==0.8.0', 'jiter==0.6.1', 'joblib==1.4.2', 'jsonpatch==1.33', 'jsonpointer==3.0.0', 'jsonschema==4.23.0', 'jsonschema-specifications==2024.10.1', 'keyring==25.5.0', 'kiwisolver==1.4.7', 'langchain==0.3.9', 'langchain-community==0.3.9', 'langchain-core==0.3.21', 'langchain-text-splitters==0.3.2', 'langsmith==0.1.147', 'lxml==5.3.0', 'markdown-it-py==3.0.0', 'markdownify==0.13.1', 'marshmallow==3.23.1', 'matplotlib==3.9.2', 'mdurl==0.1.2', 'mistral_common==1.5.1', 'more-itertools==10.5.0', 'multidict==6.1.0', 'mypy-extensions==1.0.0', 'nh3==0.2.19', 'numpy==1.26.4', 'ollama==0.3.3',
                 'orjson==3.10.12', 'packaging==24.1', 'pandas==2.2.3', 'pillow==10.4.0', 'pkginfo==1.12.0', 'playwright==1.49.0', 'propcache==0.2.1', 'pybind11==2.13.6', 'pycparser==2.22', 'pydantic==2.9.2', 'pydantic-settings==2.6.1', 'pydantic_core==2.23.4', 'pyee==12.0.0', 'Pygments==2.18.0', 'pyparsing==3.2.0', 'python-dateutil==2.9.0.post0', 'python-docx==1.1.2', 'python-dotenv==1.0.1', 'pytz==2024.2', 'PyYAML==6.0.2', 'readme_renderer==44.0', 'referencing==0.35.1', 'regex==2024.11.6', 'requests==2.32.3', 'requests-toolbelt==1.0.0', 'rfc3986==2.0.0', 'rich==13.9.4', 'rpds-py==0.22.3', 'scikit-learn==1.5.2', 'scipy==1.14.1', 'seaborn==0.13.2', 'SecretStorage==3.3.3', 'sentencepiece==0.2.0', 'six==1.16.0', 'sniffio==1.3.1', 'soupsieve==2.6', 'SQLAlchemy==2.0.36', 'strictjson==5.1.3', 'tenacity==9.0.0', 'threadpoolctl==3.5.0', 'tiktoken==0.7.0', 'tqdm==4.66.5', 'twine==6.0.1', 'typing-inspect==0.9.0', 'typing_extensions==4.12.2', 'tzdata==2024.2', 'urllib3==2.2.3', 'yarl==1.18.3', 'zipp==3.21.0']


def readme():
    """
    Load readme as long_description_content_type
    """
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name="web_page_cls",
    version="0.0.8",
    description="Web page LLM classifier and summarizer",
    long_description=readme(),
    long_description_content_type='text/markdown',
    author="Batman",
    author_email="batman@c.com",
    url="",
    license="MIT License",
    packages=["web_page_cls"] + find_packages(),
    install_requires=dependencies,
    package_data={'': ['*.json', '*.tab']}
)
