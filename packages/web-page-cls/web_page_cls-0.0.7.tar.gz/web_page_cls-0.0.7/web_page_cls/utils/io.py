"""
I/O utils
"""
import json


def read_json(json_md_path: str) -> dict:
    """
    Load from JSON
    """

    with open(json_md_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(results, json_md_path: str) -> dict:
    """
    Save to JSON
    """

    with open(json_md_path, 'w', encoding='utf-8') as f:
        json.dump(results, f)


def read_txt_file(file_path: str) -> str:
    """
    Read text file
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def write_txt_file(content: str, save_path: str):
    """
    Save content to file 
    """
    with open(save_path, 'w', encoding='utf-8') as f_save:
        f_save.write(content)
