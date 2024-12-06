"""
JSON load and save
"""
import json


def load_json(json_path):
    """
    Load from json
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(json_data, json_path):
    """
    Save data to json
    """

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False)
