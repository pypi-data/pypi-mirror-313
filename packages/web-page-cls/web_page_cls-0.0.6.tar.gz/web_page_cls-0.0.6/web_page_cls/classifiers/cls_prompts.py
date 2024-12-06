"""
Templates for LLM prompts
"""

from string import Template

web_page_classify_template = Template("""You are a classifier for web pages.
You are given informations about a web page and you have to classify it as one of the following categories:
Web page content: $content.
Generate a JSON document representing web page class like: 
{
  "web_page_class": one or couple of the most relevant web pages classes
}
Just return json. No explain.
""")

strict_cls_output_template = Template("""Label of web page, based on page content. label: Enum[$cls_str_sep_by_comma]""")

web_page_classify_strict_template = Template("""You are a classifier for web pages.
You are given informations about a web page and you have to classify it as one of the following categories:
$web_page_classes. 
                                             
Web page main content text: 
""")