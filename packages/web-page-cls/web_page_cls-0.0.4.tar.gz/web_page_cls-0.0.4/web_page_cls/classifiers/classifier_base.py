import json
from abc import ABC, abstractmethod

from strictjson import check_key, wrap_with_angle_brackets

from web_page_cls.classifiers.cls_prompts import (
    strict_cls_output_template, web_page_classify_strict_template)



class WebPageClassifier(ABC):
    """
    Base class for classifiers. Have to write own llm method
    """

    def __init__(self, web_page_classes, host="http://localhost:8000/v1", model="Qwen/Qwen2.5-3B-Instruct-AWQ") -> None:
        self.model = model
        self.host = host
        self.web_page_classes = web_page_classes

    @abstractmethod
    def llm(self, system_prompt: str, user_prompt: str):
        """
        Set method for call LLM from strict json framework
        """
        pass

    def chat(self, system_prompt: str, user_prompt: str, verbose=False):
        """
        Based on strictjson chat
        """
        res = self.llm(system_prompt=system_prompt, user_prompt=user_prompt)

        if verbose:
            print('System prompt:', system_prompt)
            print('\nUser prompt:', user_prompt)
            print('\nGPT response:', res)

        return res

    def strict_json(self, system_prompt: str, user_prompt: str,
                    output_format: dict, return_as_json=False,
                    custom_checks: dict = None,
                    check_data=None, delimiter: str = '###',
                    num_tries: int = 3):
        r""" 
        Strictjson analog for class and Ollama only

        Inputs (compulsory):
        - system_prompt: String. Write in whatever you want GPT to become. e.g. "You are a \<purpose in life\>"
        - user_prompt: String. The user input. Later, when we use it as a function, this is the function input
        - output_format: Dict. JSON format with the key as the output key, and the value as the output description

        Inputs (optional):
        - return_as_json: Bool. Default: False. Whether to return the output as a json. If False, returns as Python dict. If True, returns as json string
        - custom_checks: Dict. Key is output key, value is function which does checking of content for output field
        - check_data: Any data type. The additional data for custom_checks to use if required
        - delimiter: String (Default: '###'). This is the delimiter to surround the keys. With delimiter ###, key becomes ###key###
        - num_tries: Integer (default: 3). The number of tries to iteratively prompt GPT to generate correct json format
        - openai_json_mode: Boolean (default: False). Whether or not to use OpenAI JSON Mode
        - **kwargs: Dict. Additional arguments for LLM chat

        Output:
        - res: Dict. The JSON output of the model. Returns {} if JSON parsing failed.
        """
        # default initialise custom_checks to {}
        if custom_checks is None:
            custom_checks = {}

        # start off with no error message
        error_msg = ''

        # wrap the values with angle brackets and wrap keys with delimiter to encourage LLM to modify it
        new_output_format = wrap_with_angle_brackets(
            output_format, delimiter, 1)

        output_format_prompt = f'''\nOutput in the following json template: ```{new_output_format}```
Update values enclosed in <> and remove the <>. 
Your response must only be the updated json template beginning with {{ and ending with }}
Ensure the following output keys are present in the json: {' '.join(list(new_output_format.keys()))}'''

        for i in range(num_tries):
            my_system_prompt = str(system_prompt) + \
                output_format_prompt + error_msg
            my_user_prompt = str(user_prompt)

            # Use OpenAI to get a response
            res = self.chat(my_system_prompt, my_user_prompt)

            # extract only the chunk including the opening and closing braces
            # generate the { or } if LLM has forgotten to do so
            startindex = res.find('{')
            if startindex == -1:
                startindex = 0
                res = '{' + res
            endindex = res.rfind('}')
            if endindex == -1:
                res = res + '}'
                endindex = len(res) - 1

            res = res[startindex: endindex+1]

            # try-catch block to ensure output format is adhered to
            try:
                # check that res is a json string
                if res[0] != '{' or res[-1] != '}':
                    raise Exception(
                        'Ensure output must be a json string beginning with { and ending with }')

                # do checks for keys and output format, remove escape characters so code can be run
                end_dict = check_key(
                    res, output_format, new_output_format, delimiter, delimiter_num=1)

                # run user defined custom checks now
                for key in end_dict:
                    if key in custom_checks:
                        for check in custom_checks[key]:
                            requirement, requirement_met, action_needed = check(
                                end_dict[key], check_data)
                            print(
                                f'Running check for "{requirement}" on output field of "{key}"')
                            if not requirement_met:
                                print(
                                    f'Requirement not met. Action needed: "{action_needed}"\n\n')
                                raise Exception(
                                    f'Output field of "{key}" does not meet requirement "{requirement}". Action needed: "{action_needed}"')
                            else:
                                print('Requirement met\n\n')
                if return_as_json:
                    return json.dumps(end_dict, ensure_ascii=False)
                else:
                    return end_dict

            except Exception as e:
                error_msg = f"\n\nPrevious json: {res}\njson error: {str(e)}\nFix the error."
                print("An exception occurred:", str(e))
                print("Current invalid json format:", res)

        return {}

    def predict(self, web_page_md: str, num_tries=1):
        """
        Use strictjson to validate LLM outputs
        """
        web_page_cls_str = ', '.join(list(self.web_page_classes.values()))

        strict_cls_output_format = {'label': strict_cls_output_template.substitute(
            {'cls_str_sep_by_comma': web_page_cls_str})}

        res = self.strict_json(system_prompt=web_page_classify_strict_template.substitute({'web_page_classes': web_page_cls_str.lower()}),
                               user_prompt=web_page_md,
                               output_format=strict_cls_output_format,
                               num_tries=num_tries)

        return res
