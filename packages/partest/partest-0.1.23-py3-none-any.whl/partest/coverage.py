import re
from functools import wraps
from typing import Callable
from uuid import UUID

from confpartest import swagger_files
from partest.call_storage import call_count, call_type
from partest.parparser import SwaggerSettings

swagger_settings = SwaggerSettings(swagger_files)
paths_info = swagger_settings.collect_paths_info()

def track_api_calls(func: Callable) -> Callable:
    """Decorator for tracking API calls."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        method = args[1]
        endpoint = args[2]
        test_type = kwargs.get('type', 'unknown')

        # Collect path parameters and their enums from paths_info
        path_params = {}
        for path in paths_info:
            for param in path['parameters']:
                if param.type == 'path':
                    if param.name not in path_params:
                        if param.schema is not None and 'enum' in param.schema:
                            path_params[param.name] = param.schema['enum']
                        else:
                            path_params[param.name] = []

        # Handle add_url parameters
        for i in range(1, 4):
            add_url = kwargs.get(f'add_url{i}')
            if add_url:
                new_param = re.sub(r'^/', '', add_url)  # Remove leading slash
                matched = False
                for param_name, enum_values in path_params.items():
                    # Check if the new_param is a valid enum value for path parameters
                    if new_param in enum_values:
                        endpoint += '/{' + f'{param_name}' + '}'
                        matched = True
                        break

                if not matched:
                    # If no match was found, try adding remaining path parameters
                    if len(path_params) == 1:
                        for param_name in path_params.keys():
                            endpoint += '/{' + f'{param_name}' + '}'
                    else:
                        # Add all parameters if they are not already in the endpoint
                        for param_name in path_params.keys():
                            if param_name not in endpoint:
                                endpoint += '/{' + f'{param_name}' + '}'
                    break

        # Match method and endpoint against all paths_info
        if method is not None and endpoint is not None:
            found_match = False
            for path in paths_info:
                # Simplifying matching by using regex for dynamic segments
                regex_path = re.sub(r'\{[^}]+\}', '[^/]+', path['path'])
                if path['method'] == method and re.fullmatch(regex_path, endpoint):
                    key = (method, path['path'], path['description'])
                    call_count[key] = call_count.get(key, 0) + 1
                    call_type[key] = call_type.get(key, []) + [test_type]
                    found_match = True
                    break

            # Add unmatched paths with 0 calls
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