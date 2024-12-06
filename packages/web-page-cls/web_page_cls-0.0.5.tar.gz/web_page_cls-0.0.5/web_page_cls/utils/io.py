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