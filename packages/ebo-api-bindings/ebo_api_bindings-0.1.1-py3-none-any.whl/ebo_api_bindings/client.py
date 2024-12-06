from __future__ import annotations
import requests
import inspect
import os
from pathlib import Path
import re
from functools import wraps
from urllib.parse import unquote
import logging
from typing import get_type_hints
import mimetypes
from dataclasses import is_dataclass, fields
from tqdm import tqdm  # Import tqdm for progress bar
import json


def from_dict_recursive(data_class, data):
    if data is None:
        return None

    if not is_dataclass(data_class):
        return data

    kwargs = {}
    for field in fields(data_class):
        field_value = data.get(
            field.name
        )  # Get the value for the field from the input data
        if field_value is None:
            # Handle missing or null fields gracefully
            kwargs[field.name] = None
        elif is_dataclass(field.type) and isinstance(field_value, dict):
            # Nested dataclass
            kwargs[field.name] = from_dict_recursive(field.type, field_value)
        elif hasattr(field.type, "__origin__") and field.type.__origin__ is dict:
            # Handle Dict types
            key_type, value_type = field.type.__args__
            kwargs[field.name] = {
                key: (
                    from_dict_recursive(value_type, val)
                    if isinstance(val, dict)
                    else val
                )
                for key, val in (
                    field_value or {}
                ).items()  # Default to empty dict if None
            }
        elif hasattr(field.type, "__origin__") and field.type.__origin__ is list:
            # Handle List types
            inner_type = field.type.__args__[0]
            kwargs[field.name] = [
                (
                    from_dict_recursive(inner_type, item)
                    if isinstance(item, dict)
                    else item
                )
                for item in (field_value or [])  # Default to empty list if None
            ]
        else:
            # Primitive field
            kwargs[field.name] = field_value
    return data_class(**kwargs)


class File:
    def __init__(self, response: requests.Response, url: str):
        self.response = response
        self.url = url
        self.filename = self.extract_filename()

    def sanitize_filename(self, filename: str) -> str:
        """
        Sanitize the filename by making it a valid filename on the current platform.
        """
        safe_filename = Path(filename).name  # This ensures the filename is valid
        return re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", safe_filename)

    def extract_filename(self) -> str:
        """
        Extract the filename from the 'Content-Disposition' header if available,
        or fallback to the URL basename.
        """
        content_disposition = self.response.headers.get("Content-Disposition", "")
        if "attachment" in content_disposition:
            filename_star_match = re.findall(
                r"filename\*=UTF-8\'\'([^\s;]+)", content_disposition, re.IGNORECASE
            )
            if filename_star_match:
                filename = unquote(filename_star_match[0])
                return self.sanitize_filename(filename)
            filename_match = re.findall(
                r'filename="(.+?)"', content_disposition, re.IGNORECASE
            )
            if filename_match:
                return self.sanitize_filename(filename_match[0])

        return self.sanitize_filename(os.path.basename(self.url))

    def content(self):
        return self.response.content

    def save(
        self,
        path: str = None,
        dir: str = None,
        writable=None,
        chunk_size=8192,
        show_progress=False,
    ):
        """
        Save the file to disk or writable object with optional progress tracking.

        Args:
            path (str): Optional specific path or filename to save the file.
            dir (str): Optional directory to save the file. Ignored if 'path' is provided.
            writable: Optional writable object (e.g., an open file handle).
            chunk_size (int): Size of the chunks to read at once. Default is 8192 bytes.
            show_progress (bool): Whether to show a progress bar (default: False).
        """

        def write(w):
            total_size = int(self.response.headers.get("content-length", 0))
            with tqdm(
                desc=self.filename,
                total=total_size,
                unit="B",
                unit_scale=True,
                disable=not show_progress,
            ) as progress_bar:
                for chunk in self.response.iter_content(chunk_size=chunk_size):
                    if chunk:  # Filter out keep-alive new chunks
                        w.write(chunk)
                        progress_bar.update(len(chunk))

        if writable:
            write(writable)
        else:
            if path:
                save_path = path
            elif dir:
                if not os.path.exists(dir):
                    os.makedirs(dir)
                save_path = os.path.join(dir, self.filename)
            else:
                save_path = self.filename

            with open(save_path, "wb") as file:
                write(file)


def client(base_url: str, headers={}):
    global_headers = headers

    def decorator(
        route: str,
        method=None,
        multipart=False,
        prepare_cb=None,
        mock=None,
        query=None,
        files=None,
        headers=None,
    ):
        def wrapper(func):
            @wraps(func)
            def inner(*args, **kwargs):
                all_headers = global_headers | (headers or {})

                sig = inspect.signature(func)
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()

                # Get route args
                route_params = {
                    key: value
                    for key, value in bound.arguments.items()
                    if f"{{{key}}}" in route
                }

                url = route.format(**route_params)

                # Get query args
                remaining_args = {
                    key: value
                    for key, value in bound.arguments.items()
                    if key not in route_params
                }

                upload_files = None
                local_files = files
                if local_files:
                    upload_files = {}
                    for name in local_files:
                        val = bound.arguments[name]
                        mime_type, _ = mimetypes.guess_type(val)
                        if not mime_type:
                            mime_type = "application/octet-stream"

                        upload_files[name] = (val, open(val, "rb"), mime_type)
                        del remaining_args[name]

                    # for name in file_names:
                    #     upload_files[name] = (name, open(name, "rb"))
                    # for a in local_files:
                    #     del remaining_args[a]

                json_body = None

                # json body wil be set if its a 'complex' type
                query_params = {}
                for name, value in remaining_args.items():
                    annotation = sig.parameters[name].annotation
                    if annotation in {"int", "str", "float", "bool"}:
                        query_params[name] = value
                    else:
                        json_body = value

                local_method = method
                if local_method is None:
                    if json_body or upload_files:
                        local_method = "POST"
                    else:
                        local_method = "GET"

                # override urls
                local_base_url = base_url
                if url.startswith("http"):
                    local_base_url = ""

                # return type
                return_type = sig.return_annotation
                hints = get_type_hints(func)
                return_type = hints.get("return", None)

                if mock:
                    return return_type(**mock)

                url = f"{local_base_url}{url}"

                # Convert the json
                if json_body:
                    json_body = json_body.model_dump()

                logging.debug(
                    "Request details: Url=%s, Files=%s, Query=%s, Method=%s, Json=%s",
                    url,
                    upload_files,
                    query_params,
                    local_method,
                    json_body,
                )

                session = requests.Session()

                local_method = local_method.upper()  # Ensure the method is uppercase
                if local_method not in {
                    "GET",
                    "POST",
                    "PUT",
                    "DELETE",
                    "PATCH",
                    "HEAD",
                    "OPTIONS",
                }:
                    raise ValueError(f"Unsupported HTTP method: {local_method}")

                request = requests.Request(
                    method=local_method,
                    url=url,
                    headers=all_headers if all_headers else None,
                    files=upload_files if upload_files else None,
                    json=json_body if json_body else None,
                    params=query_params if query_params else None,
                )

                if prepare_cb:
                    prepare_cb(
                        session=session, request=request, bound_args=bound.arguments
                    )

                prepared_request = session.prepare_request(request)
                response = session.send(prepared_request, stream=True)

                if not response.ok:
                    logging.debug("Response=%s" % response.content)
                    response.raise_for_status()

                content_type = response.headers.get("Content-Type", "")
                logging.debug("Response content_type=%s" % content_type)

                if "application/json" in content_type:
                    response_json = response.json()
                    logging.debug("Response json=%s" % json.dumps(response_json, indent=2))

                    ### DATACLASSES
                    data = from_dict_recursive(return_type, response_json)

                    ### PYDANTIC
                    # data = return_type(**x)
                elif "text/plain" in content_type:
                    return response.text
                else:
                    data = File(response, url)
                return data

            return inner

        return wrapper

    return decorator
