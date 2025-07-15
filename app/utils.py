# app/utils.py

def flatten_json(obj, parent_key='', sep='.'):
    items = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            items.extend(flatten_json(value, new_key, sep=sep))
    elif isinstance(obj, list):
        for index, item in enumerate(obj):
            new_key = f"{parent_key}{sep}{index}" if parent_key else str(index)
            items.extend(flatten_json(item, new_key, sep=sep))
    else:
        value_str = f"{obj:.6f}" if isinstance(obj, float) else str(obj)
        items.append(f"{parent_key}: {value_str}")
    return items


def chunk_json_data(data, chunk_size=100):
    """
    Converts a list of JSON-like dictionaries into smaller flattened text chunks
    suitable for vector embedding.
    """
    chunks = []
    if isinstance(data, list):
        for record in data:
            flat = flatten_json(record)
            for i in range(0, len(flat), chunk_size):
                chunk = " || ".join(flat[i:i + chunk_size])
                chunks.append(chunk)
    return chunks
