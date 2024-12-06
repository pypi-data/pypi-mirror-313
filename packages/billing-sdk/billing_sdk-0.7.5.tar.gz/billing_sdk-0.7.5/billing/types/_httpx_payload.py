from typing import Callable, Optional, TypedDict, Union

from httpx import Limits
from httpx._types import (
    AuthTypes,
    CertTypes,
    CookieTypes,
    HeaderTypes,
    ProxiesTypes,
    ProxyTypes,
    QueryParamTypes,
    TimeoutTypes,
    VerifyTypes,
)
from typing_extensions import NotRequired


class HTTPXPayload(TypedDict):
    auth: NotRequired[Optional[AuthTypes]]
    params: NotRequired[Optional[QueryParamTypes]]
    headers: NotRequired[Optional[HeaderTypes]]
    cookies: NotRequired[Optional[CookieTypes]]
    verify: NotRequired[VerifyTypes]
    cert: NotRequired[Optional[CertTypes]]
    http1: NotRequired[bool]
    http2: NotRequired[bool]
    proxy: NotRequired[Optional[ProxyTypes]]
    proxies: NotRequired[Optional[ProxiesTypes]]
    timeout: NotRequired[TimeoutTypes]
    follow_redirects: NotRequired[bool]
    limits: NotRequired[Limits]
    max_redirects: NotRequired[int]
    trust_env: NotRequired[bool]
    default_encoding: NotRequired[Union[str, Callable[[bytes], str]]]
