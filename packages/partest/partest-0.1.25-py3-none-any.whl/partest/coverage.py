import re
from functools import wraps
from typing import Callable
from uuid import UUID

from confpartest import swagger_files
from partest.call_storage import call_count, call_type
from partest.parparser import SwaggerSettings

swagger_settings = SwaggerSettings(swagger_files)
paths_info = swagger_settings.collect_paths_info()

import re
from functools import wraps
from typing import Callable
from uuid import UUID


def track_api_calls(func: Callable) -> Callable:
    """Decorator for tracking API calls."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        method = args[1]
        endpoint = args[2]
        test_type = kwargs.get('type', 'unknown')

        path_params = {}
        for path in paths_info:
            for param in path['parameters']:
                if param.type == 'path':
                    path_params[param.name] = param.schema.get('enum', [])

        for i in range(1, 4):
            add_url = kwargs.get(f'add_url{i}')
            if add_url:
                new_param = re.sub(r'^/', '', add_url)  # Убираем ведущий слеш
                endpoint += f"/{new_param}"

        endpoint_template = endpoint
        for param_name in path_params.keys():
            endpoint_template = endpoint_template.replace(f"/{param_name}", f"/{{{param_name}}}")

        found_match = False
        for path in paths_info:
            if path['method'] == method and re.fullmatch(path['path'].replace('{fileId}', r'[^/]+'), endpoint_template):
                key = (method, path['path'], path['description'])
                call_count[key] = call_count.get(key, 0) + 1
                call_type[key] = call_type.get(key, []) + [test_type]
                found_match = True
                break

        for path in paths_info:
            key = (path['method'], path['path'], path['description'])
            if key not in call_count:
                call_count[key] = 0
                call_type[key] = []

        response = await func(*args, **kwargs)
        return response

    return wrapper

def is_valid_uuid(uuid_to_test, version=4):
    """Checks if the given string is a valid UUID."""
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test