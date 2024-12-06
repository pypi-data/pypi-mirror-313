"""
Templates for LLM prompts
"""

from string import Template

web_page_classify_template = Template("""Given a web page content in markdown format classify to one of the following web pages classes: $web_page_classes. 
                                      Web page content: $content.
                                      Generate a JSON document representing web page class like: 
{
  "web_page_class": one or couple of the most relevant web pages classes
}
Just return json. No explain.
""")

strict_cls_output_template = Template("""Label of web page, based on page content. label: Enum[$cls_str_sep_by_comma]""")

strict_cls_output_format = {'label': "Label of web page, based on page content. label: Enum['Government', 'IT company', 'E-Commerce', 'Media and News', 'Business company', 'Military', 'Bad request', 'Other']"}

web_page_classify_strict_template = Template("""Given a web page content classify to one of the following web pages labels: 
$web_page_classes. 
Just return json. No explain. """)