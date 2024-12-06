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

strict_cls_output_format = {'label': "Label of web page, based on page content. label: Enum['Government', 'IT company', 'E-Commerce', 'Media and News', 'Business company', 'Military', 'Bad request', 'Other']"}

web_page_classify_strict_template = Template("""Given a web page content classify to one of the following web pages labels: 
$web_page_classes. 

Labels description:
  Government: “Web pages belonging to government entities or agencies.”
  IT Company: “Web pages of Information Technology companies offering hardware, software, consulting services, or other tech-related products/services.”
  E-Commerce: “Web pages of online businesses facilitating buying and selling of goods.”
  Media and News: “Web pages of media outlets publishing news content.”
  Business Company: “Web pages of commercial entities aiming to earn a profit.”
  Military: “Web pages related to the armed forces of a country used for defense and combat operations”
  Bad Request: “Web pages with invalid requests due to malformed syntax or missing required fields.”
  Other: “Web pages not covered by the above categories.”
Just return json. No explain. """)