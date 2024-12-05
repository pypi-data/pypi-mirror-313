import json
import socket
import time
from dataclasses import asdict, dataclass, field
from json import JSONDecodeError
from typing import Any, cast
from urllib.parse import urlencode

import httpx
import pydash

from mm_std.result import Err, Ok, Result

FIREFOX_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0"
SAFARI_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"  # fmt: skip # noqa
CHROME_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"  # fmt: skip # noqa


@dataclass
class HResponse:
    code: int = 0
    error: str | None = None
    body: str = ""
    headers: dict[str, str] = field(default_factory=dict)

    _json_data: Any = None
    _json_parsed = False
    _json_parsed_error = False

    def _parse_json(self) -> None:
        try:
            self._json_data = None
            self._json_data = json.loads(self.body)
            self._json_parsed_error = False
        except JSONDecodeError:
            self._json_parsed_error = True
        self._json_parsed = True

    @property
    def json(self) -> Any:
        if not self._json_parsed:
            self._parse_json()
        return self._json_data

    @property
    def json_parse_error(self) -> bool:
        if not self._json_parsed:
            self._parse_json()
        return self._json_parsed_error

    @property
    def content_type(self) -> str | None:
        for key in self.headers.keys():
            if key.lower() == "content-type":
                return self.headers[key]
        return None

    def to_err_result[T](self, error: str | None = None) -> Err:
        return Err(error or self.error or "error", data=asdict(self))

    def to_ok_result[T](self, result: T) -> Result[T]:
        return Ok(result, data=asdict(self))

    def is_error(self) -> bool:
        return self.error is not None

    def is_timeout_error(self) -> bool:
        return self.error == "timeout"

    def is_proxy_error(self) -> bool:
        return self.error == "proxy_error"

    def is_connection_error(self) -> bool:
        return self.error is not None and self.error.startswith("connection_error:")

    def to_dict(self) -> dict[str, Any]:
        return pydash.omit(asdict(self), "_json_data")


def hrequest(
    url: str,
    *,
    method: str = "GET",
    proxy: str | None = None,
    params: dict[str, Any] | None = None,
    headers: dict[str, Any] | None = None,
    cookies: dict[str, Any] | None = None,
    timeout: float = 10,
    user_agent: str | None = None,
    json_params: bool = True,
    auth: Any = None,
    verify: bool = True,
) -> HResponse:
    query_params: dict[str, Any] | None = None
    data: dict[str, Any] | None = None
    json_: dict[str, Any] | None = None
    method = method.upper()
    if not headers:
        headers = {}
    if user_agent:
        headers["user-agent"] = user_agent
    if method == "GET":
        query_params = params
    elif json_params:
        json_ = params
    else:
        data = params

    try:
        r = httpx.request(
            method,
            url,
            proxy=proxy,
            timeout=timeout,
            cookies=cookies,
            auth=auth,
            verify=verify,
            headers=headers,
            params=query_params,
            json=json_,
            data=data,
        )
        return HResponse(code=r.status_code, body=r.text, headers=dict(r.headers))
    except httpx.TimeoutException:
        return HResponse(error="timeout")
    except httpx.ProxyError:
        return HResponse(error="proxy_error")
    except httpx.HTTPError as err:
        return HResponse(error=f"connection_error: {err}")
    except Exception as err:
        return HResponse(error=f"exception: {err}")


def check_port(ip: str, port: int, attempts: int = 3, sleep_seconds: float = 1, timeout: float = 1) -> bool:
    for _ in range(attempts):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        res = sock.connect_ex((ip, port)) == 0
        if res:
            return True
        time.sleep(sleep_seconds)
    return False


def get_free_local_port() -> int:
    sock = socket.socket()
    sock.bind(("", 0))
    port = sock.getsockname()[1]
    sock.close()
    return cast(int, port)


def add_query_params_to_url(url: str, params: dict[str, object]) -> str:
    query_params = urlencode({k: v for k, v in params.items() if v is not None})
    if query_params:
        url += f"?{query_params}"
    return url


hr = hrequest
