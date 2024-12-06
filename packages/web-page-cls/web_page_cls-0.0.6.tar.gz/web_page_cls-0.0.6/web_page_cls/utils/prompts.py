"""
Templates for LLM prompts
"""

from string import Template

web_page_what_a_page_template = Template("""Given a web page content in markdown describe it.
                                      Web page content: $content.""")

clean_prompt_template = Template(
    """Please make summary of web page. Web page: $content.""")

web_page_annotate_template = Template("""Given a web page content in markdown format summarize it in one or two sentenses.
                                      Web page content: $content. Summary:""")
