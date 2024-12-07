from datetime import datetime, date
import json


class JSON:
    # Remove callable objects from the data and serialize datetimes.
    def serialize(obj):
        if isinstance(obj, dict):
            return {k: JSON.serialize(v) for k, v in obj.items() if not callable(v)}
        elif isinstance(obj, list):
            return [JSON.serialize(item) for item in obj if not callable(item)]
        elif isinstance(obj, datetime) or isinstance(obj, date):
            return obj.isoformat()
        elif callable(obj):
            return None
        else:
            return obj

    def stringify(data):
        cleaned_data = JSON.serialize(data)
        return json.dumps(cleaned_data)

    def remove_keys(data: dict, keys_to_ignore: list[str]):
        return {k: v for k, v in data.items() if k not in keys_to_ignore}

    def parse(data):
        return json.loads(data)
