"""
pyupbit-for-devs package:
   Copyright 2024 Sanghoon Lee (DSsoli). All Rights Reserved.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Modifications, Additions, and Deletions:
    - Additions: trade_utils.py for Robust API/Function Calls with correct response assurance and retries
    - Deletions: pyupbit's custom error handlings
    - Modifications: functions in quotation_api.py, request_api.py, and exchange_api.py,
        in order to show raw and detailed response from Upbit API directly for debugging purposes.

Base code for pyupbit-for-devs package (pyupbit):
   Copyright 2021 Jonghun Yoo, Brayden Jo, pystock/pyquant (sharebook-kr), (et al.). All Rights Reserved.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


import re
import requests
from requests import Response
from typing import Any, Tuple, Dict, Optional
import json

HTTP_RESP_CODE_START = 200
HTTP_RESP_CODE_END = 400


def _parse(remaining_req: str) -> Dict[str, Any]:
    """Parse the number of remaining requests info for Upbit API

    Args:
        remaining_req (str): String of the number of remaining requests info
         like "group=market; min=573; sec=9"
    Returns:
        Parsed dictionary of the number of remaining requests info
         like {'group': 'market', 'min': 573, 'sec': 2}
    Raises:
        ValueError: If remaining_req pattern search returns None for match.
        Exception: If error occurs while parsing input.
    """
    try:
        pattern = re.compile(r"group=([a-z\-]+); min=([0-9]+); sec=([0-9]+)")
        matched = pattern.search(remaining_req)
        if matched is None:
            raise ValueError(f"{remaining_req} pattern search returned None for match")

        ret = {
            "group": matched.group(1),
            "min": int(matched.group(2)),
            "sec": int(matched.group(3)),
        }
        return ret
    except (AttributeError, ValueError) as e:
        raise Exception(f"Error parsing input. Error: {e}")


def _call_get(url: str, **kwargs: Any) -> Response:
    return requests.get(url, **kwargs)


def _call_post(url: str, **kwargs: Any) -> Response:
    return requests.post(url, **kwargs)


def _call_delete(url: str, **kwargs: Any) -> Response:
    return requests.delete(url, **kwargs)


def _call_public_api(url: str, **params: Any) -> Tuple[Any, Dict[str, Any]]:
    """Call Upbit public api

    Args:
        url (str): REST API url
        params (any): GET method parameters
    Returns:
        The contents of requested url, parsed remaining requests count info
    """
    resp = _call_get(url, params=params)
    data = resp.json()
    remaining_req = resp.headers.get("Remaining-Req", "")
    limit = _parse(remaining_req)
    return data, limit


def _send_post_request(
    url: str, headers: Dict[str, str], data: Dict[str, Any]
) -> Tuple[Any, Dict[str, Any]]:
    """Call POST method request for Upbit

    Args:
        url (str): REST API url
        headers (dict[str, str]): HTTP headers
        data (dict[str, any]): Data
    Returns:
        The contents of requested url, parsed remaining requests count info
    """
    if isinstance(headers, dict):
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"

    if isinstance(data, dict):
        data = json.dumps(data)

    resp = _call_post(url, headers=headers, data=data)
    data = resp.json()
    remaining_req = resp.headers.get("Remaining-Req", "")
    limit = _parse(remaining_req)
    return data, limit


def _send_get_request(url, headers, data=None):
    """Call GET method request for Upbit

    Args:
        url (str): REST API url
        headers (dict[str, str]): HTTP headers
        data (dict[str, any]): Data
    Returns:
        The contents of requested url, parsed remaining requests count info
    """
    resp = _call_get(url, headers=headers, data=data)
    data = resp.json()
    remaining_req = resp.headers.get("Remaining-Req", "")
    limit = _parse(remaining_req)
    return data, limit


def _send_delete_request(
    url: str, headers: Dict[str, str], data: Dict[str, Any]
) -> Optional[Tuple[Any, Dict[str, Any]]]:
    """Call DELETE method request for Upbit

    Args:
        url (str): REST API url
        headers (dict[str, str]): HTTP headers
        data (dict[str, any]): Data
    Returns:
        The contents of requested url, parsed remaining requests count info
    """
    if isinstance(headers, dict):
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"

    if isinstance(data, dict):
        data = json.dumps(data)

    resp = _call_delete(url, headers=headers, data=data)
    data = resp.json()
    remaining_req = resp.headers.get("Remaining-Req", "")
    limit = _parse(remaining_req)
    return data, limit
