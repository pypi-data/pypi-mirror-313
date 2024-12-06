import os
import json


def read_cache(cache_file_name='image_cache.json'):
    """
    Read image cache
    """
    if os.path.exists(cache_file_name):
        with open(cache_file_name, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return {}


def dump_cache(cache_json, cache_file_name='image_cache.json'):
    """
    Dump image cache to json
    """
    with open(cache_file_name, 'w', encoding='utf-8') as f:
        return json.dump(cache_json, f, ensure_ascii=False)
